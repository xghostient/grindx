"""Code editor with auto-indent, line operations, clipboard, and Esc passthrough."""

import re
from textual.widgets import TextArea
from textual.events import Key

from ..clipboard import copy_to_clipboard, paste_from_clipboard

# Keys that the editor should NOT handle — route to screen actions instead
_PASSTHROUGH = {
    "ctrl+d": "mark_done",
    "ctrl+b": "toggle_bookmark",
    "ctrl+t": "toggle_timer",
    "ctrl+r": "reset_timer",
    "ctrl+l": "toggle_lang",
    "ctrl+e": "evaluate",
}


class CodeEditor(TextArea):

    def _on_key(self, event: Key) -> None:
        if event.key == "escape":
            event.stop()
            event.prevent_default()
            self.screen.action_go_back()
            return

        if event.key in _PASSTHROUGH:
            event.stop()
            event.prevent_default()
            action = _PASSTHROUGH[event.key]
            if hasattr(self.screen, f"action_{action}"):
                getattr(self.screen, f"action_{action}")()
            return

        # Clipboard: Ctrl+Shift+C to copy, Ctrl+Shift+V to paste
        if event.key == "ctrl+shift+c":
            event.stop()
            event.prevent_default()
            self._copy_selection()
            return

        if event.key == "ctrl+shift+v":
            event.stop()
            event.prevent_default()
            self._paste_clipboard()
            return

        # Alt+Up/Down: move line, Alt+Shift+Down: duplicate line
        if event.key == "alt+up":
            event.stop()
            event.prevent_default()
            self._move_line(-1)
            return

        if event.key == "alt+down":
            event.stop()
            event.prevent_default()
            self._move_line(1)
            return

        if event.key == "alt+shift+down":
            event.stop()
            event.prevent_default()
            self._duplicate_line()
            return

        if event.key == "enter":
            row, _col = self.cursor_location
            current_line = self.document.get_line(row)
            indent = re.match(r"^(\s*)", current_line).group(1)
            stripped = current_line.rstrip()
            if stripped.endswith(":") or stripped.endswith("{"):
                indent += "    "
            event.stop()
            event.prevent_default()
            self.insert("\n" + indent)
            return

        super()._on_key(event)

    # ─── Clipboard ───

    def _copy_selection(self) -> None:
        """Copy selected text to system clipboard."""
        text = self.selected_text
        if text:
            copy_to_clipboard(text)

    def _paste_clipboard(self) -> None:
        """Paste from system clipboard at cursor."""
        text = paste_from_clipboard()
        if text:
            self.insert(text)

    # ─── Line operations ───

    def _move_line(self, direction: int) -> None:
        """Move current line up (-1) or down (+1)."""
        row, col = self.cursor_location
        line_count = self.document.line_count
        target = row + direction
        if target < 0 or target >= line_count:
            return
        lines = self.text.split("\n")
        lines[row], lines[target] = lines[target], lines[row]
        self.text = "\n".join(lines)
        self.cursor_location = (target, col)

    def _duplicate_line(self) -> None:
        """Duplicate current line below."""
        row, col = self.cursor_location
        lines = self.text.split("\n")
        lines.insert(row + 1, lines[row])
        self.text = "\n".join(lines)
        self.cursor_location = (row + 1, col)
