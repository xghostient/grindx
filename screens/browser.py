"""Main browser screen — topic list + problem list."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, ListView
from textual.screen import Screen

from data import (
    load_sheet, load_enriched, load_progress, slug_from_name,
    make_stub_problem, short_topic, get_solution_path,
)
from widgets import TopicItem, ProblemItem


class ProblemBrowser(Screen):
    BINDINGS = [
        Binding("q", "quit_app", "Quit"),
        Binding("escape", "go_back", "Back"),
        Binding("right", "focus_right", show=False),
        Binding("left", "focus_left", show=False),
        Binding("e", "filter_easy", "Easy"),
        Binding("m", "filter_medium", "Medium"),
        Binding("h", "filter_hard", "Hard"),
        Binding("a", "filter_all", "All"),
        Binding("b", "filter_bookmarked", "Bookmarked"),
        Binding("s", "show_stats", "Stats"),
    ]

    CSS = """
    #browser-container { height: 1fr; }

    #topic-list {
        width: 32;
        border-right: solid $accent;
        height: 1fr;
    }

    #problem-list {
        width: 1fr;
        height: 1fr;
    }

    TopicItem { height: 3; padding: 0 1; }
    ProblemItem { height: 2; padding: 0 1; }

    #progress-bar {
        height: 3;
        padding: 1;
        background: $surface;
        text-align: center;
    }

    #filter-bar {
        height: 1;
        padding: 0 1;
        background: $boost;
    }

    #sheet-name-bar {
        height: 1;
        padding: 0 1;
        background: $accent;
    }
    """

    def __init__(self, sheet: dict):
        super().__init__()
        self.sheet = sheet
        self.all_topics = load_sheet(sheet["path"])
        self.progress = load_progress()
        self.topic_keys = list(self.all_topics.keys())
        self.current_topic = None
        self.difficulty_filter = None
        self._enriched_cache: dict[str, dict[str, dict] | None] = {}
        self._problem_list_index: int | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            f"  {self.sheet['name']}  ({self.sheet['count']} problems)",
            id="sheet-name-bar",
        )
        yield Static(self._filter_bar_text(), id="filter-bar")
        with Horizontal(id="browser-container"):
            yield ListView(*self._build_topic_items(), id="topic-list")
            yield ListView(id="problem-list")
        yield Static(self._build_progress_text(), id="progress-bar")
        yield Footer()

    # ─── Data helpers ───

    def _get_enriched(self, topic_key: str) -> dict[str, dict] | None:
        if topic_key not in self._enriched_cache:
            self._enriched_cache[topic_key] = load_enriched(topic_key)
        return self._enriched_cache[topic_key]

    def _get_problem_obj(self, topic_key: str, name: str) -> dict:
        enriched = self._get_enriched(topic_key)
        if enriched:
            slug = slug_from_name(name)
            if slug in enriched:
                return enriched[slug]
            for p in enriched.values():
                if slug_from_name(p.get("name", "")) == slug:
                    return p
        return make_stub_problem(name, topic_key)

    def _filtered_names(self, topic_key: str) -> list[str]:
        names = self.all_topics.get(topic_key, [])
        if not self.difficulty_filter:
            return names
        result = []
        for n in names:
            pid = slug_from_name(n)
            if self.difficulty_filter == "Bookmarked":
                if self.progress.get(pid, {}).get("bookmarked", False):
                    result.append(n)
            else:
                prob = self._get_problem_obj(topic_key, n)
                if prob.get("difficulty") == self.difficulty_filter:
                    result.append(n)
        return result

    # ─── Build UI ───

    def _filter_bar_text(self) -> str:
        f = self.difficulty_filter
        parts = []
        for key, label in [
            (None, "All"), ("Easy", "Easy"), ("Medium", "Medium"),
            ("Hard", "Hard"), ("Bookmarked", "Bookmarked"),
        ]:
            shortcut = {"All": "a", "Easy": "e", "Medium": "m", "Hard": "h", "Bookmarked": "b"}[label]
            if f == key:
                parts.append(f"[reverse] {shortcut}:{label} [/]")
            else:
                parts.append(f"[{shortcut}]{label}")
        return " Filter: " + "  ".join(parts) + "  |  [s]Stats"

    def _build_topic_items(self) -> list[TopicItem]:
        items = []
        for key in self.topic_keys:
            filtered = self._filtered_names(key)
            if self.difficulty_filter and not filtered:
                continue
            total = len(filtered)
            done = sum(
                1 for n in filtered
                if self.progress.get(slug_from_name(n), {}).get("solved", False)
            )
            items.append(TopicItem(key, total, done))
        return items

    def _build_progress_text(self) -> str:
        total = sum(len(v) for v in self.all_topics.values())
        done = sum(
            1
            for names in self.all_topics.values()
            for n in names
            if self.progress.get(slug_from_name(n), {}).get("solved", False)
        )
        pct = int(done / total * 100) if total > 0 else 0
        filled = pct // 5
        bar = "█" * filled + "░" * (20 - filled)
        topic_display = ""
        if self.current_topic:
            topic_display = f"  [{short_topic(self.current_topic)}]"
        filt = f"  Filter: {self.difficulty_filter}" if self.difficulty_filter else ""
        return f"  Progress: {done}/{total}  {bar}  {pct}%{topic_display}{filt}"

    def _refresh_problem_list(self):
        if not self.current_topic:
            return
        problem_list = self.query_one("#problem-list", ListView)
        problem_list.clear()
        for name in self._filtered_names(self.current_topic):
            prob = self._get_problem_obj(self.current_topic, name)
            pid = prob["id"]
            solved = self.progress.get(pid, {}).get("solved", False)
            bookmarked = self.progress.get(pid, {}).get("bookmarked", False)
            started = not solved and (
                get_solution_path(pid, "Python").exists()
                or get_solution_path(pid, "Go").exists()
            )
            problem_list.append(ProblemItem(prob, solved, started, bookmarked))

    def _refresh_topic_list(self):
        topic_list = self.query_one("#topic-list", ListView)
        topic_list.clear()
        for item in self._build_topic_items():
            topic_list.append(item)

    # ─── Events ───

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item is None:
            return
        if isinstance(event.item, TopicItem):
            self.current_topic = event.item.topic_key
            self._refresh_problem_list()
            self.query_one("#progress-bar", Static).update(self._build_progress_text())

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, TopicItem):
            self.query_one("#problem-list", ListView).focus()
        elif isinstance(item, ProblemItem):
            problem_list = self.query_one("#problem-list", ListView)
            self._problem_list_index = problem_list.index
            from screens.solve import SolveScreen
            self.app.push_screen(SolveScreen(item.problem, self.progress))

    # ─── Filters ───

    def _apply_filter(self, filt):
        self.difficulty_filter = filt
        self._refresh_topic_list()
        self._refresh_problem_list()
        self.query_one("#filter-bar", Static).update(self._filter_bar_text())
        self.query_one("#progress-bar", Static).update(self._build_progress_text())

    def action_filter_easy(self):
        self._apply_filter("Easy" if self.difficulty_filter != "Easy" else None)

    def action_filter_medium(self):
        self._apply_filter("Medium" if self.difficulty_filter != "Medium" else None)

    def action_filter_hard(self):
        self._apply_filter("Hard" if self.difficulty_filter != "Hard" else None)

    def action_filter_all(self):
        self._apply_filter(None)

    def action_filter_bookmarked(self):
        self._apply_filter("Bookmarked" if self.difficulty_filter != "Bookmarked" else None)

    def action_show_stats(self):
        from screens.stats import StatsScreen
        all_problems = []
        for key, names in self.all_topics.items():
            for n in names:
                all_problems.append(self._get_problem_obj(key, n))
        self.app.push_screen(StatsScreen(all_problems, self.progress, self.all_topics))

    # ─── Navigation ───

    def action_focus_right(self):
        self.query_one("#problem-list", ListView).focus()

    def action_focus_left(self):
        self.query_one("#topic-list", ListView).focus()

    def action_quit_app(self):
        self.app.exit()

    def action_go_back(self):
        focused = self.focused
        topic_list = self.query_one("#topic-list", ListView)
        if focused is topic_list:
            # Go back to welcome screen
            self.app.pop_screen()
        else:
            topic_list.focus()

    def _restore_problem_index(self) -> None:
        problem_list = self.query_one("#problem-list", ListView)
        if self._problem_list_index is not None:
            problem_list.index = self._problem_list_index
        problem_list.focus()

    def on_screen_resume(self) -> None:
        self.progress = load_progress()
        self._refresh_topic_list()
        self.query_one("#filter-bar", Static).update(self._filter_bar_text())
        self.query_one("#progress-bar", Static).update(self._build_progress_text())
        self._refresh_problem_list()
        self.set_timer(0.05, self._restore_problem_index)
