"""Cross-platform clipboard helpers (macOS, Linux, Windows)."""

import subprocess
import sys


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard. Returns True on success."""
    if sys.platform == "darwin":
        cmds = [["pbcopy"]]
    elif sys.platform == "win32":
        cmds = [["clip"]]
    else:
        cmds = [
            ["xclip", "-selection", "clipboard"],
            ["xsel", "--clipboard", "--input"],
        ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, input=text.encode(), check=True, timeout=2)
            return True
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    return False


def paste_from_clipboard() -> str | None:
    """Read text from system clipboard. Returns None on failure."""
    if sys.platform == "darwin":
        cmds = [["pbpaste"]]
    elif sys.platform == "win32":
        cmds = [["powershell", "-command", "Get-Clipboard"]]
    else:
        cmds = [
            ["xclip", "-selection", "clipboard", "-o"],
            ["xsel", "--clipboard", "--output"],
        ]
    for cmd in cmds:
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=2)
            if result.returncode == 0:
                return result.stdout.decode()
        except (FileNotFoundError, subprocess.SubprocessError):
            continue
    return None
