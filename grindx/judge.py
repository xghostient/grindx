"""Judge orchestrator — runs user code against test cases in a subprocess."""

import json
import os
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

_JUDGE_FILENAME = {
    "java": "Judge.java",
}

_COMPILED_LANGS = {"cpp", "java", "go"}

def _compile_cmd(lang_dir: str, judge_name: str, tmp: Path) -> list[str]:
    """Build the compile command for a compiled language."""
    if lang_dir == "cpp":
        return ["g++", "-O2", "-std=c++17", "-I.", "-o", f"judge{_EXE_SUFFIX}", judge_name]
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

    # --- Load time limit from test case (clamped to 0.5-30s) ---
    try:
        with open(tc_path) as f:
            tc_meta = json.load(f)
        time_limit = max(0.5, min(float(tc_meta.get("time_limit_s", 5)), 30.0))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        time_limit = 5.0

    result = _execute_judge(lang_dir, problem_id, tc_path, j_path, common_path, sol_path, time_limit)
    if result.verdict != "TLE":
        return result
    if result.cases_total > 0:
        return result
    if not _supports_prefix_progress(j_path):
        return result
    passed, total = _estimate_tle_progress(
        problem_id=problem_id,
        lang_dir=lang_dir,
        tc_path=tc_path,
        j_path=j_path,
        common_path=common_path,
        sol_path=sol_path,
        time_limit=time_limit,
    )
    if total <= 0:
        return result
    result.cases_passed = passed
    result.cases_total = total
    return result


def _execute_judge(
    lang_dir: str,
    problem_id: str,
    tc_path: Path,
    j_path: Path,
    common_path: Path | None,
    sol_path: Path,
    time_limit: float,
) -> JudgeResult:
    start = time.monotonic()
    sol_filename = _SOLUTION_FILENAME.get(lang_dir, f"solution{sol_path.suffix}")
    judge_filename = _JUDGE_FILENAME.get(lang_dir, j_path.name)

    with tempfile.TemporaryDirectory(prefix="grindx_") as tmpdir:
        tmp = Path(tmpdir)

        shutil.copy2(tc_path, tmp / f"{problem_id}.json")
        shutil.copy2(j_path, tmp / judge_filename)
        shutil.copy2(sol_path, tmp / sol_filename)
        if common_path and common_path.exists():
            shutil.copy2(common_path, tmp / common_path.name)
            if lang_dir == "cpp":
                cpp_bits_dir = common_path.parent / "bits"
                if cpp_bits_dir.exists():
                    shutil.copytree(cpp_bits_dir, tmp / "bits", dirs_exist_ok=True)

        if lang_dir == "go":
            (tmp / "go.mod").write_text("module judge\n\ngo 1.21\n")

        if lang_dir in _COMPILED_LANGS:
            compile_c = _compile_cmd(lang_dir, judge_filename, tmp)
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
                    verdict="CE",
                    cases_passed=0,
                    cases_total=0,
                    error="Compilation timed out.",
                    total_time_ms=(time.monotonic() - start) * 1000,
                )
            if compile_result.returncode != 0:
                return JudgeResult(
                    verdict="CE",
                    cases_passed=0,
                    cases_total=0,
                    error=compile_result.stderr[:2000],
                    total_time_ms=(time.monotonic() - start) * 1000,
                )

        cmd = _run_cmd(lang_dir, judge_filename, sol_filename, tmp)
        if not cmd:
            return JudgeResult(
                verdict="ERR",
                cases_passed=0,
                cases_total=0,
                error=f"Unsupported language: {lang_dir}",
            )

        progress_path = tmp / "__grindx_progress__.json"
        env = os.environ.copy()
        env["GRINDX_PROGRESS_FILE"] = str(progress_path)
        if time_limit <= 1:
            exec_timeout = time_limit + 0.1
        elif time_limit <= 2:
            exec_timeout = time_limit + 0.5
        elif time_limit <= 5:
            exec_timeout = time_limit + 1
        else:
            exec_timeout = time_limit + 2
        try:
            proc = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=exec_timeout,
                preexec_fn=_make_preexec(),
                env=env,
            )
        except subprocess.TimeoutExpired as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            passed, total = _read_progress(progress_path)
            if total <= 0:
                passed, total = _parse_progress_markers(_coerce_text(exc.stdout))
            return JudgeResult(
                verdict="TLE",
                cases_passed=passed,
                cases_total=total,
                error=f"Process killed after {time_limit:g}s.",
                total_time_ms=elapsed_ms,
            )
        progress_snapshot = _read_progress(progress_path)

    elapsed_ms = (time.monotonic() - start) * 1000
    if proc.returncode == 0:
        result = _parse_stdout(proc.stdout)
        return JudgeResult(
            verdict="AC",
            cases_passed=result.get("passed", 0),
            cases_total=result.get("total", 0),
            total_time_ms=elapsed_ms,
        )
    if proc.returncode == 1:
        result = _parse_stdout(proc.stdout)
        if not result or "total" not in result or "passed" not in result:
            stderr = proc.stderr.strip()[:2000] if proc.stderr else ""
            stdout = proc.stdout.strip()[:2000] if proc.stdout else ""
            return _runtime_error_result(
                tc_path=tc_path,
                progress=progress_snapshot,
                error=stderr or stdout or "Judge exited with code 1 without emitting a verdict.",
                total_time_ms=elapsed_ms,
            )
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
    stderr = proc.stderr.strip()[:2000] if proc.stderr else ""
    return _runtime_error_result(
        tc_path=tc_path,
        progress=progress_snapshot,
        error=stderr or "Runtime error (no details captured).",
        total_time_ms=elapsed_ms,
    )


def _supports_prefix_progress(j_path: Path) -> bool:
    try:
        text = j_path.read_text().lower()
    except OSError:
        return False
    blocked_tokens = (
        "generate_large_cases",
        "generatelargecases",
        "generate_large_rotate_cases",
        "largecases",
        "large_cases",
        "largecase",
        "large input",
        "cases.addall",
        "concat(generatelargecases",
        "tc[\"cases\"] +",
        "tc.cases.concat",
    )
    return not any(token in text for token in blocked_tokens)


def _coerce_text(output: str | bytes | None) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output


def _runtime_error_result(
    tc_path: Path,
    progress: tuple[int, int],
    error: str,
    total_time_ms: float,
) -> JudgeResult:
    passed, total = progress
    visible_cases = _load_visible_cases(tc_path)
    visible_total = len(visible_cases)
    if total <= 0:
        total = visible_total
    failed_case = passed if total > 0 else None
    input_preview = ""
    category = ""
    if failed_case is not None:
        if failed_case < visible_total:
            case = visible_cases[failed_case]
            input_preview = _preview_value(case.get("input"))
            category = str(case.get("category", ""))
        elif visible_total > 0:
            input_preview = "<hidden generated case>"
            category = "hidden"
    return JudgeResult(
        verdict="RE",
        cases_passed=passed,
        cases_total=total,
        failed_case=failed_case,
        input_preview=input_preview,
        category=category,
        error=error,
        total_time_ms=total_time_ms,
    )


def _load_visible_cases(tc_path: Path) -> list[dict]:
    try:
        with open(tc_path) as f:
            tc_data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []
    cases = tc_data.get("cases")
    if not isinstance(cases, list):
        return []
    return [case for case in cases if isinstance(case, dict)]


def _preview_value(value) -> str:
    try:
        text = json.dumps(value)
    except TypeError:
        text = str(value)
    if len(text) <= 200:
        return text
    return text[:197] + "..."


def _read_progress(progress_path: Path) -> tuple[int, int]:
    try:
        payload = progress_path.read_text().strip()
    except OSError:
        return 0, 0
    if not payload or "," not in payload:
        return 0, 0
    passed_str, total_str = payload.split(",", 1)
    try:
        passed = int(passed_str)
        total = int(total_str)
    except ValueError:
        return 0, 0
    return passed, total


def _parse_progress_markers(stdout: str) -> tuple[int, int]:
    passed = 0
    total = 0
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line.startswith("__GRINDX_PROGRESS__"):
            continue
        payload = line[len("__GRINDX_PROGRESS__"):]
        try:
            progress = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if not isinstance(progress, dict):
            continue
        next_passed = progress.get("passed")
        next_total = progress.get("total")
        if isinstance(next_passed, int) and isinstance(next_total, int):
            passed = next_passed
            total = next_total
    return passed, total


def _estimate_tle_progress(
    problem_id: str,
    lang_dir: str,
    tc_path: Path,
    j_path: Path,
    common_path: Path | None,
    sol_path: Path,
    time_limit: float,
) -> tuple[int, int]:
    try:
        with open(tc_path) as f:
            tc_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return 0, 0
    cases = tc_data.get("cases")
    if not isinstance(cases, list):
        return 0, 0
    total = len(cases)
    if total == 0:
        return 0, 0
    low = 0
    high = total
    with tempfile.TemporaryDirectory(prefix="grindx_tle_") as tmpdir:
        prefix_tc = Path(tmpdir) / f"{problem_id}.json"
        while low < high:
            mid = (low + high + 1) // 2
            tc_data["cases"] = cases[:mid]
            prefix_tc.write_text(json.dumps(tc_data))
            result = _execute_judge(lang_dir, problem_id, prefix_tc, j_path, common_path, sol_path, time_limit)
            if result.verdict == "AC":
                low = mid
            elif result.verdict == "TLE":
                high = mid - 1
            else:
                return 0, total
    return low, total


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
