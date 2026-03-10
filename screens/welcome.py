"""Welcome screen — sheet selection."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label
from textual.screen import Screen

from data import list_sheets, load_progress


class SheetItem(ListItem):
    def __init__(self, sheet: dict, done: int) -> None:
        super().__init__()
        self.sheet = sheet
        self.done = done

    def compose(self) -> ComposeResult:
        total = self.sheet["count"]
        pct = int(self.done / total * 100) if total > 0 else 0
        filled = pct // 5
        bar = "█" * filled + "░" * (20 - filled)
        yield Label(
            f"  {self.sheet['name']}\n"
            f"    {self.done}/{total}  {bar}  {pct}%"
        )


class WelcomeScreen(Screen):
    BINDINGS = [
        Binding("q", "quit_app", "Quit"),
    ]

    CSS = """
    #welcome-container {
        align: center middle;
        height: 1fr;
    }

    #welcome-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
    }

    #welcome-subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
        width: 100%;
    }

    #sheet-list {
        width: 60;
        height: auto;
        max-height: 80%;
        margin: 0 4;
    }

    SheetItem {
        height: 4;
        padding: 0 2;
    }

    #welcome-hint {
        text-align: center;
        color: $text-muted;
        margin-top: 2;
        width: 100%;
    }
    """

    def __init__(self):
        super().__init__()
        self.sheets = list_sheets()
        self.progress = load_progress()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            "\n[bold]  grindx[/bold]",
            id="welcome-title", markup=True,
        )
        yield Static(
            "  Distraction-free DSA practice in your terminal",
            id="welcome-subtitle",
        )
        items = []
        for sheet in self.sheets:
            done = self._count_done(sheet)
            items.append(SheetItem(sheet, done))
        yield ListView(*items, id="sheet-list")
        yield Static(
            "  ↑↓ navigate  Enter select  q quit",
            id="welcome-hint",
        )
        yield Footer()

    def _count_done(self, sheet: dict) -> int:
        from data import load_sheet
        topics = load_sheet(sheet["path"])
        count = 0
        for ids in topics.values():
            for pid in ids:
                if self.progress.get(pid, {}).get("solved", False):
                    count += 1
        return count

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, SheetItem):
            from screens.browser import ProblemBrowser
            self.app.push_screen(ProblemBrowser(item.sheet))

    def action_quit_app(self):
        self.app.exit()
