"""Welcome screen — sheet selection."""

import calendar
import hashlib
from datetime import date, timedelta

from collections import Counter

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label
from textual.screen import Screen

from ..data import list_sheets, load_progress, load_all_problems, get_problem, fmt_duration


class DailyItem(ListItem):
    def __init__(self, problem: dict, solved: bool) -> None:
        super().__init__()
        self.problem = problem
        self.solved = solved

    def compose(self) -> ComposeResult:
        diff = self.problem.get("difficulty", "")
        diff_color = {"Easy": "green", "Medium": "yellow", "Hard": "red"}.get(diff, "white")
        marker = "[green]✓[/]" if self.solved else "○"
        yield Label(
            f"  ⚡ Daily Problem\n"
            f"    {marker}  [{diff_color}]{diff}[/]  {self.problem['name']}",
            markup=True,
        )


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
        Binding("escape", "quit_app", "Quit", show=False),
        Binding("s", "show_stats", "Stats"),
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

    #welcome-main {
        height: auto;
        max-height: 80%;
        align: center middle;
    }

    #sheet-list {
        width: 50;
        height: auto;
        max-height: 100%;
    }

    #activity-pane {
        width: 40;
        height: auto;
        padding: 1 2;
    }

    DailyItem {
        height: 4;
        padding: 0 2;
        background: $primary-background;
    }

    SheetItem {
        height: 4;
        padding: 0 2;
    }

    #welcome-stats {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
        width: 100%;
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
        yield Static(self._build_stats_summary(), id="welcome-stats")
        items = []
        daily = self._get_daily_problem()
        if daily:
            solved = self.progress.get(daily["id"], {}).get("solved", False)
            items.append(DailyItem(daily, solved))
        for sheet in self.sheets:
            done = self._count_done(sheet)
            items.append(SheetItem(sheet, done))
        with Horizontal(id="welcome-main"):
            yield ListView(*items, id="sheet-list", initial_index=0)
            yield Static(self._build_activity(), id="activity-pane")
        yield Static(
            "  ↑↓ navigate  Enter select  s stats  q quit",
            id="welcome-hint",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.set_timer(0.05, self._focus_list)

    def _focus_list(self) -> None:
        sheet_list = self.query_one("#sheet-list", ListView)
        sheet_list.index = 0
        sheet_list.focus()

    def _count_done(self, sheet: dict) -> int:
        from ..data import load_sheet
        topics = load_sheet(sheet["path"])
        count = 0
        for ids in topics.values():
            for pid in ids:
                if self.progress.get(pid, {}).get("solved", False):
                    count += 1
        return count

    def _build_stats_summary(self) -> str:
        problems = load_all_problems()
        total = len(problems)
        solved = sum(
            1 for pid in problems
            if self.progress.get(pid, {}).get("solved", False)
        )
        today_str = date.today().isoformat()
        today_count = sum(
            1 for pdata in self.progress.values()
            if pdata.get("solved") and pdata.get("solved_date") == today_str
        )
        streak = self._calc_streak()
        parts = [f"  {solved}/{total} solved"]
        if streak > 0:
            parts.append(f"{streak} day streak")
        if today_count > 0:
            parts.append(f"Today: {today_count} solved")
        return "  " + "  |  ".join(parts)

    def _calc_streak(self) -> int:
        solve_dates = set()
        for pdata in self.progress.values():
            if pdata.get("solved") and pdata.get("solved_date"):
                solve_dates.add(pdata["solved_date"])
        if not solve_dates:
            return 0
        today = date.today()
        streak = 0
        d = today
        while d.isoformat() in solve_dates:
            streak += 1
            d -= timedelta(days=1)
        if streak == 0:
            yesterday = today - timedelta(days=1)
            if yesterday.isoformat() in solve_dates:
                streak = 1
                d = yesterday - timedelta(days=1)
                while d.isoformat() in solve_dates:
                    streak += 1
                    d -= timedelta(days=1)
        return streak

    def _build_activity(self) -> str:
        solve_counts = Counter()
        for pdata in self.progress.values():
            if pdata.get("solved") and pdata.get("solved_date"):
                solve_counts[pdata["solved_date"]] += 1
        today = date.today()
        lines = [f"[bold]{today.strftime('%B %Y')}[/bold]\n"]
        lines.append(" Mo Tu We Th Fr Sa Su")
        cal = calendar.monthcalendar(today.year, today.month)
        for week in cal:
            row = " "
            for day in week:
                if day == 0:
                    row += "   "
                else:
                    d = date(today.year, today.month, day)
                    count = solve_counts.get(d.isoformat(), 0)
                    ds = f"{day:2d}"
                    if d == today:
                        if count > 6:
                            row += f"[reverse bold green]{ds}[/] "
                        elif count >= 3:
                            row += f"[reverse green]{ds}[/] "
                        elif count >= 1:
                            row += f"[reverse #2d6a2d]{ds}[/] "
                        else:
                            row += f"[reverse]{ds}[/] "
                    elif count > 6:
                        row += f"[bold green]{ds}[/] "
                    elif count >= 3:
                        row += f"[green]{ds}[/] "
                    elif count >= 1:
                        row += f"[#2d6a2d]{ds}[/] "
                    else:
                        row += f"[dim]{ds}[/] "
            lines.append(row)
        lines.append(f"\n[#2d6a2d]1-2[/] [green]3-6[/] [bold green]6+[/]  [reverse]today[/]")
        return "\n".join(lines)

    def _get_daily_problem(self) -> dict | None:
        problems = load_all_problems()
        if not problems:
            return None
        all_ids = sorted(problems.keys())
        # Same problem for all users on a given day
        seed = hashlib.md5(date.today().isoformat().encode()).hexdigest()
        idx = int(seed, 16) % len(all_ids)
        return problems[all_ids[idx]]

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, DailyItem):
            from .solve import SolveScreen
            self.app.push_screen(SolveScreen(item.problem, self.progress))
        elif isinstance(item, SheetItem):
            from .browser import ProblemBrowser
            self.app.push_screen(ProblemBrowser(item.sheet))

    def on_screen_resume(self) -> None:
        self.progress = load_progress()
        self.query_one("#welcome-stats", Static).update(self._build_stats_summary())
        self.query_one("#activity-pane", Static).update(self._build_activity())
        sheet_list = self.query_one("#sheet-list", ListView)
        sheet_list.clear()
        daily = self._get_daily_problem()
        if daily:
            solved = self.progress.get(daily["id"], {}).get("solved", False)
            sheet_list.append(DailyItem(daily, solved))
        for sheet in self.sheets:
            done = self._count_done(sheet)
            sheet_list.append(SheetItem(sheet, done))

    def action_show_stats(self):
        from ..data import load_sheet
        from .stats import StatsScreen
        all_problems = []
        all_topics = {}
        seen = set()
        for sheet in self.sheets:
            topics = load_sheet(sheet["path"])
            for key, ids in topics.items():
                for pid in ids:
                    if pid not in seen:
                        seen.add(pid)
                        all_problems.append(get_problem(pid))
                if key not in all_topics:
                    all_topics[key] = ids
        self.app.push_screen(StatsScreen(all_problems, self.progress, all_topics))

    def action_quit_app(self):
        self.app.exit()
