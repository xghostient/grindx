"""List items for topics and problems."""

from textual.app import ComposeResult
from textual.widgets import ListItem, Label


class TopicItem(ListItem):
    def __init__(self, topic_key: str, total: int, done: int) -> None:
        super().__init__()
        self.topic_key = topic_key
        self.total = total
        self.done = done

    def compose(self) -> ComposeResult:
        pct = int(self.done / self.total * 100) if self.total > 0 else 0
        filled = pct // 10
        bar = "█" * filled + "░" * (10 - filled)
        display = self.topic_key.split(" - ", 1)[-1] if " - " in self.topic_key else self.topic_key
        yield Label(f"{display}\n  {self.done}/{self.total} {bar} {pct}%")


class ProblemItem(ListItem):
    def __init__(self, problem: dict, solved: bool, started: bool, bookmarked: bool) -> None:
        super().__init__()
        self.problem = problem
        self.solved = solved
        self.started = started
        self.bookmarked = bookmarked

    def compose(self) -> ComposeResult:
        if self.solved:
            marker = "[green]✓[/]"
        elif self.started:
            marker = "[yellow]◐[/]"
        else:
            marker = "○"
        bm = " ★" if self.bookmarked else ""
        diff = self.problem.get("difficulty", "")
        if diff in ("Easy", "Medium", "Hard"):
            diff_color = {"Easy": "green", "Medium": "yellow", "Hard": "red"}[diff]
            diff_tag = f"[{diff_color}]{diff:<6}[/] "
        else:
            diff_tag = "       "
        safe_name = self.problem['name'].replace("[", "\\[")
        yield Label(
            f" {marker}  {diff_tag}{safe_name}{bm}",
            markup=True,
        )
