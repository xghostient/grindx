"""Stats dashboard screen."""

from collections import Counter
from datetime import date, timedelta
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from ..data import short_topic, fmt_duration, name_from_slug


class StatsScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("q", "go_back", "Back"),
    ]

    CSS = """
    #stats-container {
        padding: 2 4;
        height: 1fr;
        overflow-y: auto;
    }
    .stats-section { margin-bottom: 1; }
    #stats-title {
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }
    """

    def __init__(self, problems: list[dict], progress: dict, all_topics: dict[str, list[str]]):
        super().__init__()
        self.problems = problems
        self.progress = progress
        self.all_topics = all_topics

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="stats-container"):
            yield Static("[bold]── Stats Dashboard ──[/bold]", id="stats-title", markup=True)

            # Overall
            total = len(self.problems)
            solved = sum(1 for p in self.problems if self.progress.get(p["id"], {}).get("solved", False))
            bookmarked = sum(1 for p in self.problems if self.progress.get(p["id"], {}).get("bookmarked", False))
            pct = int(solved / total * 100) if total > 0 else 0
            filled = pct // 5
            bar = "█" * filled + "░" * (20 - filled)
            yield Static(
                f"  Overall: {solved}/{total}  {bar}  {pct}%\n  Bookmarked: {bookmarked}",
                classes="stats-section",
            )

            # By difficulty
            lines = "\n  [bold]By Difficulty:[/bold]"
            for diff in ["Easy", "Medium", "Hard"]:
                dp = [p for p in self.problems if p.get("difficulty") == diff]
                ds = sum(1 for p in dp if self.progress.get(p["id"], {}).get("solved", False))
                dt = len(dp)
                pc = int(ds / dt * 100) if dt > 0 else 0
                color = {"Easy": "green", "Medium": "yellow", "Hard": "red"}[diff]
                f = pc // 10
                b = "█" * f + "░" * (10 - f)
                lines += f"\n  [{color}]{diff:<6}[/]  {ds}/{dt}  {b}  {pc}%"
            yield Static(lines, classes="stats-section", markup=True)

            # By topic
            tlines = "\n  [bold]By Topic:[/bold]"
            for key in self.all_topics:
                ids = self.all_topics[key]
                ts = sum(1 for pid in ids if self.progress.get(pid, {}).get("solved", False))
                tt = len(ids)
                tp = int(ts / tt * 100) if tt > 0 else 0
                f = tp // 10
                b = "█" * f + "░" * (10 - f)
                tlines += f"\n  {short_topic(key):<30}  {ts}/{tt}  {b}  {tp}%"
            yield Static(tlines, classes="stats-section", markup=True)

            # Streak
            solve_dates = set()
            for pdata in self.progress.values():
                if pdata.get("solved") and pdata.get("solved_date"):
                    solve_dates.add(pdata["solved_date"])
            streak = self._calc_streak(solve_dates)
            yield Static(
                f"\n  [bold]Current Streak: {streak} day{'s' if streak != 1 else ''}[/bold]",
                markup=True,
            )

            # Activity calendar
            solve_counts = Counter()
            for pdata in self.progress.values():
                sd = pdata.get("solved_date")
                if sd:
                    solve_counts[sd] += 1
            cal = self._build_calendar(solve_counts)
            yield Static(cal, classes="stats-section", markup=True)

            # Best times
            times = []
            for pid, pdata in self.progress.items():
                if pid.startswith("_"):
                    continue
                if pdata.get("best_time"):
                    pname = next((p["name"] for p in self.problems if p["id"] == pid), name_from_slug(pid))
                    times.append((pname, pdata["best_time"]))
            if times:
                tl = "\n  [bold]Best Times:[/bold]"
                times.sort(key=lambda x: x[1])
                for name, t in times[:10]:
                    tl += f"\n  {name:<35} {fmt_duration(t)}"
                yield Static(tl, classes="stats-section", markup=True)

            yield Static("\n  [dim]Press Esc to go back[/dim]", markup=True)
        yield Footer()

    def _build_calendar(self, solve_counts: Counter) -> str:
        """Build a 12-week activity calendar like GitHub's contribution graph."""
        today = date.today()
        # Start from 11 weeks ago on Monday
        start = today - timedelta(days=today.weekday(), weeks=11)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        lines = ["\n  [bold]Activity (12 weeks):[/bold]\n"]

        # Header — 3-char month labels aligned to 3-char-wide columns
        header = "      "
        prev_month = ""
        for week in range(12):
            d = start + timedelta(weeks=week)
            month = d.strftime("%b")
            if month != prev_month:
                header += month
                prev_month = month
            else:
                header += "   "
        lines.append(f"  {header}")

        # One row per weekday — 3-char-wide columns (symbol + 2 spaces)
        for dow in range(7):
            label = days[dow][0] + " " if dow % 2 == 0 else "  "
            row = f"  {label}   "
            for week in range(12):
                d = start + timedelta(weeks=week, days=dow)
                if d > today:
                    row += "[dim]·[/]  "
                else:
                    count = solve_counts.get(d.isoformat(), 0)
                    if count == 0:
                        row += "[dim]░[/]  "
                    elif count == 1:
                        row += "[green]▒[/]  "
                    elif count <= 3:
                        row += "[green]▓[/]  "
                    else:
                        row += "[green]█[/]  "
            lines.append(row)

        lines.append("\n    [dim]░[/]=none  [green]▒[/]=1  [green]▓[/]=2-3  [green]█[/]=4+")
        return "\n".join(lines)

    def _calc_streak(self, solve_dates: set[str]) -> int:
        if not solve_dates:
            return 0
        today = date.today()
        streak = 0
        d = today
        while d.isoformat() in solve_dates:
            streak += 1
            d = date.fromordinal(d.toordinal() - 1)
        if streak == 0:
            yesterday = date.fromordinal(today.toordinal() - 1)
            if yesterday.isoformat() in solve_dates:
                streak = 1
                d = date.fromordinal(yesterday.toordinal() - 1)
                while d.isoformat() in solve_dates:
                    streak += 1
                    d = date.fromordinal(d.toordinal() - 1)
        return streak

    def action_go_back(self):
        self.app.pop_screen()
