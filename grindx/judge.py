"""Judge orchestrator — runs user code against test cases in a subprocess."""

import json
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from .data import (
    LANG_DIR,
    get_solution_path,
    judge_common_path,
    judge_path,
    testcase_path,
)


@dataclass
class JudgeResult:
    verdict: str  # AC, WA, TLE, RE, CE, ERR
    cases_passed: int
    cases_total: int
    failed_case: int | None = None
    input_preview: str = ""
    expected_preview: str = ""
    actual_preview: str = ""
    error: str = ""
    category: str = ""
    total_time_ms: float = 0.0


# ---------------------------------------------------------------------------
# Language-specific configuration
# ---------------------------------------------------------------------------

_EXE_SUFFIX = ".exe" if sys.platform == "win32" else ""

# How to name the solution file in the temp directory per language.
# Java requires class name == file name; Go needs .go extension in package main.
_SOLUTION_FILENAME = {
    "python": "solution.py",
    "cpp": "solution.cpp",
    "java": "Solution.java",
    "javascript": "solution.js",
    "go": "solution.go",
}

_COMPILED_LANGS = {"cpp", "java", "go"}


def _compile_cmd(lang_dir: str, judge_name: str, tmp: Path) -> list[str]:
    """Build the compile command for a compiled language."""
    if lang_dir == "cpp":
        return ["g++", "-O2", "-std=c++17", "-o", f"judge{_EXE_SUFFIX}", judge_name]
    elif lang_dir == "java":
        java_files = [f.name for f in tmp.glob("*.java")]
        return ["javac"] + java_files
    elif lang_dir == "go":
        return ["go", "build", "-o", f"judge{_EXE_SUFFIX}", "."]
    return []


def _run_cmd(lang_dir: str, judge_name: str, sol_filename: str, tmp: Path) -> list[str]:
    """Build the run command for any language."""
    if lang_dir == "python":
        return [sys.executable, str(tmp / judge_name), str(tmp / sol_filename)]
    elif lang_dir == "javascript":
        return ["node", str(tmp / judge_name), str(tmp / sol_filename)]
    elif lang_dir == "cpp" or lang_dir == "go":
        return [str(tmp / f"judge{_EXE_SUFFIX}")]
    elif lang_dir == "java":
        # All Java judges use class name "Judge" (package-private)
        return ["java", "-cp", ".", "Judge"]
    return []


# ---------------------------------------------------------------------------
# Resource limits (best-effort, Unix only)
# ---------------------------------------------------------------------------

def _make_preexec(memory_mb: int = 512):
    """Return a preexec_fn that sets resource limits, or None on Windows."""
    if sys.platform == "win32":
        return None

    def _set_limits():
        try:
            import resource
            soft = memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (soft, -1))
        except (ImportError, ValueError, OSError):
            pass

    return _set_limits


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_tests(problem_id: str, lang: str) -> JudgeResult:
    """Run the judge for a problem in a given language. Returns JudgeResult."""
    lang_dir = LANG_DIR[lang]

    # --- Resolve all paths ---
    tc_path = testcase_path(problem_id)
    if tc_path is None:
        return JudgeResult(
            verdict="ERR", cases_passed=0, cases_total=0,
            error="No test cases available for this problem.",
        )

    j_path = judge_path(problem_id, lang_dir)
    if j_path is None:
        return JudgeResult(
            verdict="ERR", cases_passed=0, cases_total=0,
            error=f"No judge available for {lang}.",
        )

    common_path = judge_common_path(lang_dir)

    sol_path = get_solution_path(problem_id, lang)
    if not sol_path.exists():
        return JudgeResult(
            verdict="ERR", cases_passed=0, cases_total=0,
            error="No solution saved. Save your code first (Ctrl+S).",
        )

    # --- Load time limit from test case (clamped to 1-30s) ---
    try:
        with open(tc_path) as f:
            tc_meta = json.load(f)
        time_limit = max(1, min(int(tc_meta.get("time_limit_s", 5)), 30))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        time_limit = 5

    # --- Run in temp directory ---
    start = time.monotonic()
    sol_filename = _SOLUTION_FILENAME.get(lang_dir, f"solution{sol_path.suffix}")

    with tempfile.TemporaryDirectory(prefix="grindx_") as tmpdir:
        tmp = Path(tmpdir)

        # Copy files into the sandbox
        shutil.copy2(tc_path, tmp / f"{problem_id}.json")
        shutil.copy2(j_path, tmp / j_path.name)
        shutil.copy2(sol_path, tmp / sol_filename)
        if common_path and common_path.exists():
            shutil.copy2(common_path, tmp / common_path.name)

        # Go needs a go.mod in the temp directory
        if lang_dir == "go":
            (tmp / "go.mod").write_text("module judge\n\ngo 1.21\n")

        # --- Compile if needed ---
        if lang_dir in _COMPILED_LANGS:
            compile_c = _compile_cmd(lang_dir, j_path.name, tmp)
            try:
                compile_result = subprocess.run(
                    compile_c,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            except subprocess.TimeoutExpired:
                return JudgeResult(
                    verdict="CE", cases_passed=0, cases_total=0,
                    error="Compilation timed out.",
                    total_time_ms=(time.monotonic() - start) * 1000,
                )
            if compile_result.returncode != 0:
                return JudgeResult(
                    verdict="CE", cases_passed=0, cases_total=0,
                    error=compile_result.stderr[:2000],
                    total_time_ms=(time.monotonic() - start) * 1000,
                )

        # --- Build run command ---
        cmd = _run_cmd(lang_dir, j_path.name, sol_filename, tmp)
        if not cmd:
            return JudgeResult(
                verdict="ERR", cases_passed=0, cases_total=0,
                error=f"Unsupported language: {lang}",
            )

        # --- Execute judge subprocess ---
        try:
            proc = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=time_limit + 2,  # small buffer over per-case limit
                preexec_fn=_make_preexec(),
            )
        except subprocess.TimeoutExpired:
            elapsed_ms = (time.monotonic() - start) * 1000
            return JudgeResult(
                verdict="TLE", cases_passed=0, cases_total=0,
                error=f"Process killed after {time_limit}s.",
                total_time_ms=elapsed_ms,
            )

    elapsed_ms = (time.monotonic() - start) * 1000

    # --- Parse result ---
    if proc.returncode == 0:
        # AC
        result = _parse_stdout(proc.stdout)
        return JudgeResult(
            verdict="AC",
            cases_passed=result.get("passed", 0),
            cases_total=result.get("total", 0),
            total_time_ms=elapsed_ms,
        )
    elif proc.returncode == 1:
        # WA
        result = _parse_stdout(proc.stdout)
        return JudgeResult(
            verdict="WA",
            cases_passed=result.get("passed", 0),
            cases_total=result.get("total", 0),
            failed_case=result.get("failed_case"),
            input_preview=result.get("input_preview", ""),
            expected_preview=result.get("expected_preview", ""),
            actual_preview=result.get("actual_preview", ""),
            category=result.get("category", ""),
            total_time_ms=elapsed_ms,
        )
    else:
        # RE (runtime error)
        stderr = proc.stderr.strip()[:2000] if proc.stderr else ""
        return JudgeResult(
            verdict="RE", cases_passed=0, cases_total=0,
            error=stderr or "Runtime error (no details captured).",
            total_time_ms=elapsed_ms,
        )


def _parse_stdout(stdout: str) -> dict:
    """Parse the JSON verdict from judge stdout.

    The verdict is always the last line. Earlier lines may contain
    debug output from the user's solution (print statements, etc.).
    """
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return {}
