"""Test result screen — displays judge verdict."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from ..judge import JudgeResult

_VERDICT_STYLE = {
    "AC": ("green", "Accepted"),
    "WA": ("red", "Wrong Answer"),
    "TLE": ("yellow", "Time Limit Exceeded"),
    "RE": ("red", "Runtime Error"),
    "CE": ("red", "Compilation Error"),
    "ERR": ("red", "Error"),
}

_VERDICT_ICON = {
    "AC": "✓",
    "WA": "✗",
    "TLE": "⏱",
    "RE": "!",
    "CE": "!",
    "ERR": "?",
}


def _build_detail_text(result: JudgeResult) -> str:
    """Build the detail text shown below the verdict banner."""
    lines: list[str] = []

    if result.verdict == "AC":
        lines.append(
            f"Passed {result.cases_passed}/{result.cases_total} test cases"
            f"  ·  {result.total_time_ms:.0f}ms"
        )

    elif result.verdict == "WA":
        lines.append(f"Passed {result.cases_passed}/{result.cases_total} test cases")
        if result.failed_case is not None:
            cat = f" ({result.category})" if result.category else ""
            lines.append(f"\nFailed on case {result.failed_case + 1}{cat}:")
            lines.append(f"  Input:    {result.input_preview}")
            lines.append(f"  Expected: {result.expected_preview}")
            lines.append(f"  Got:      {result.actual_preview}")

    elif result.verdict == "TLE":
        lines.append(result.error)

    elif result.verdict in ("RE", "CE"):
        if result.error:
            lines.append(result.error[:1000])

    elif result.verdict == "ERR":
        lines.append(result.error or "Unknown error.")

    return "\n".join(lines)


class TestResultScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("r", "retry", "Retry"),
    ]

    CSS = """
    #test-scroll {
        padding: 1 2;
        overflow-y: auto;
        height: 1fr;
    }
    #test-banner {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
        padding: 1 0;
    }
    #test-details {
        height: auto;
        padding: 0 2;
    }
    #test-bar {
        height: 1;
        padding: 0 1;
        background: $surface;
    }
    """

    def __init__(self, result: JudgeResult, problem: dict):
        super().__init__()
        self.result = result
        self.problem = problem

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        color, label = _VERDICT_STYLE.get(
            self.result.verdict, ("white", self.result.verdict)
        )
        icon = _VERDICT_ICON.get(self.result.verdict, "?")
        with Vertical(id="test-scroll"):
            yield Static(
                f"[{color} bold]{icon}  {label}[/]",
                id="test-banner",
                markup=True,
            )
            yield Static(
                _build_detail_text(self.result),
                id="test-details",
            )
        yield Static(
            " r: Retry  |  Esc: Back",
            id="test-bar",
        )
        yield Footer()

    def action_retry(self) -> None:
        self.dismiss("retry")

    def action_go_back(self) -> None:
        self.app.pop_screen()
