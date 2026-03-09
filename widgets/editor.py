"""Code editor with auto-indent and Esc passthrough."""

import re
from textual.widgets import TextArea
from textual.events import Key

# Keys that the editor should NOT handle — route to screen actions instead
_PASSTHROUGH = {
    "ctrl+d": "mark_done",
    "ctrl+b": "toggle_bookmark",
    "ctrl+t": "toggle_timer",
    "ctrl+r": "reset_timer",
    "ctrl+l": "toggle_lang",
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
