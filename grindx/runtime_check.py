"""Runtime detection — check which language compilers/interpreters are installed."""

import shutil
import sys

# Command used to verify each language runtime is available.
_RUNTIME_CMDS: dict[str, str] = {
    "python": sys.executable,
    "cpp": "g++",
    "java": "javac",
    "javascript": "node",
    "go": "go",
}


def detect_runtimes() -> dict[str, bool]:
    """Return {lang_dir: available} for every supported language."""
    result: dict[str, bool] = {}
    for lang, cmd in _RUNTIME_CMDS.items():
        if lang == "python":
            result[lang] = True  # always available — we're running in it
        else:
            result[lang] = shutil.which(cmd) is not None
    return result


def runtime_available(lang_dir: str) -> bool:
    """Check whether a single language runtime is installed."""
    cmd = _RUNTIME_CMDS.get(lang_dir)
    if cmd is None:
        return False
    if lang_dir == "python":
        return True
    return shutil.which(cmd) is not None
