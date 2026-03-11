"""AI evaluation result screen."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Markdown
from textual.screen import Screen

from ..clipboard import copy_to_clipboard

_SEPARATORS = ["---HINTS---", "--- HINTS ---", "---hints---"]


def _split_hints(response: str) -> tuple[str, str]:
    """Split response into main content and hints."""
    # Try explicit separators first
    for sep in _SEPARATORS:
        if sep in response:
            parts = response.split(sep, 1)
            return parts[0].strip(), parts[1].strip()
    # Fall back to splitting on ## Hints header
    for marker in ["\n## Hints\n", "\n## Hints\r\n", "\n##Hints\n"]:
        if marker in response:
            idx = response.index(marker)
            return response[:idx].strip(), response[idx:].strip()
    return response, ""


class EvaluateScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("ctrl+y", "copy", "Copy"),
        Binding("h", "toggle_hints", "Hints"),
    ]

    CSS = """
    #eval-scroll {
        padding: 1 2;
        overflow-y: auto;
        height: 1fr;
    }
    #eval-title {
        text-style: bold;
        margin-bottom: 1;
    }
    #eval-content { height: auto; }
    #eval-hints { height: auto; margin-top: 1; }
    #eval-bar {
        height: 1;
        padding: 0 1;
        background: $surface;
    }
    """

    def __init__(self, problem_name: str, response: str):
        super().__init__()
        self.problem_name = problem_name
        self._response = response
        self._hints_visible = False

        self._main, self._hints = _split_hints(response)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="eval-scroll"):
            yield Static(
                f"[bold]AI Review — {self.problem_name}[/bold]",
                id="eval-title", markup=True,
            )
            yield Markdown(self._main, id="eval-content")
            yield Markdown("", id="eval-hints")
        hint_label = "h: Show hints" if self._hints else ""
        yield Static(
            f" ^Y: Copy  {hint_label}  |  Esc: Back",
            id="eval-bar",
        )
        yield Footer()

    def action_toggle_hints(self):
        if not self._hints:
            return
        self._hints_visible = not self._hints_visible
        hints_widget = self.query_one("#eval-hints", Markdown)
        if self._hints_visible:
            hints_widget.update(self._hints)
            label = "h: Hide hints"
        else:
            hints_widget.update("")
            label = "h: Show hints"
        self.query_one("#eval-bar", Static).update(
            f" ^Y: Copy  {label}  |  Esc: Back"
        )

    def action_copy(self):
        full = self._response if self._hints_visible else self._main
        if copy_to_clipboard(full):
            self.query_one("#eval-bar", Static).update(
                " ✓ Copied!  |  Esc: Back"
            )
        else:
            self.query_one("#eval-bar", Static).update(
                " Copy failed  |  Esc: Back"
            )

    def action_go_back(self):
        self.app.pop_screen()
