"""Solve screen — problem description + code editor."""

import time
from datetime import date
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

from ..data import (
    load_solution, save_solution, load_progress,
    save_progress, fmt_duration,
    TEMPLATE_KEY, LANG_ORDER, EDITOR_LANG,
)
from ..widgets import CodeEditor


class SolveScreen(Screen):
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+d", "mark_done", "Done"),
        Binding("ctrl+e", "evaluate", "AI Review"),
        Binding("ctrl+l", "toggle_lang", "Lang"),
        Binding("ctrl+b", "toggle_bookmark", "Bookmark", show=False),
        Binding("ctrl+t", "toggle_timer", "Timer", show=False),
        Binding("ctrl+r", "reset_timer", "Reset", show=False),
    ]

    CSS = """
    #solve-container { height: 1fr; }

    #problem-pane {
        width: 45%;
        padding: 1 2;
        border-right: solid $accent;
        overflow-y: auto;
        height: 1fr;
    }

    #code-pane { width: 55%; height: 1fr; }

    #problem-title { text-style: bold; margin-bottom: 1; }
    #problem-difficulty { margin-bottom: 1; }
    #problem-desc { margin-bottom: 1; }
    #example-section { margin-bottom: 1; }
    #constraints-section { color: $text-muted; }

    #lang-indicator {
        height: 1;
        padding: 0 1;
        background: $primary;
        color: $text;
        text-align: right;
    }

    #code-editor { height: 1fr; }

    #status-bar {
        height: 1;
        padding: 0 1;
        background: $surface;
    }

    #timer-bar {
        height: 1;
        padding: 0 1;
        background: $surface-darken-1;
    }
    """

    def __init__(self, problem: dict, progress: dict):
        super().__init__()
        self.problem = problem
        self.progress = progress
        self.lang = "Python"
        self._initial_code = ""
        self._timer_running = False
        self._timer_start = 0.0
        self._timer_elapsed = 0.0
        self._timer_interval = None

    def on_mount(self) -> None:
        # Auto-start timer when opening a problem
        self._timer_start = time.monotonic()
        self._timer_running = True
        self._timer_interval = self.set_interval(1.0, self._tick_timer)
        self._update_timer_display()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        pid = self.problem["id"]
        best = self.progress.get(pid, {}).get("best_time")
        best_str = f"  |  Best: {fmt_duration(best)}" if best else ""
        yield Static(f" ▶ Timer: 0m 00s{best_str}  [^T pause  ^R reset]", id="timer-bar")
        with Horizontal(id="solve-container"):
            with Vertical(id="problem-pane"):
                diff = self.problem.get("difficulty", "?")
                diff_color = {"Easy": "green", "Medium": "yellow", "Hard": "red"}.get(diff, "white")
                bm = self.progress.get(pid, {}).get("bookmarked", False)
                bm_str = "  ★ Bookmarked" if bm else ""
                yield Static(
                    f"[bold]{self.problem['name']}[/bold]{bm_str}",
                    id="problem-title", markup=True,
                )
                yield Static(
                    f"[{diff_color}]● {diff}[/]  |  {self.problem.get('category', '')}",
                    id="problem-difficulty", markup=True,
                )
                yield Static(self.problem.get("description", ""), id="problem-desc")
                examples_text = self._format_examples()
                if examples_text:
                    yield Static(examples_text, id="example-section")
                constraints = self.problem.get("constraints", "")
                if constraints:
                    yield Static(f"Constraints: {constraints}", id="constraints-section")
            with Vertical(id="code-pane"):
                yield Static(f"  Language: {self.lang}", id="lang-indicator")
                code = self._load_or_template()
                yield CodeEditor(
                    code,
                    language="python",
                    id="code-editor",
                    tab_behavior="indent",
                    show_line_numbers=True,
                    theme="dracula",
                )
        solved = self.progress.get(pid, {}).get("solved", False)
        status = "✓ SOLVED" if solved else "○ UNSOLVED"
        yield Static(
            f" {status}  |  ^S Save  ^D Done  ^E AI  ^L Lang  ^B Bookmark  |  Esc: Back",
            id="status-bar",
        )
        yield Footer()

    def _format_examples(self) -> str:
        examples = self.problem.get("examples", [])
        if not examples:
            return ""
        lines = ["─── Examples ───"]
        for i, ex in enumerate(examples, 1):
            lines.append(f"\nExample {i}:")
            lines.append(f"  Input:  {ex['input']}")
            lines.append(f"  Output: {ex['output']}")
        return "\n".join(lines)

    def _load_or_template(self) -> str:
        saved = load_solution(self.problem["id"], self.lang)
        if saved:
            self._initial_code = saved
            return saved
        template_key = TEMPLATE_KEY[self.lang]
        template = self.problem.get(template_key, "")
        self._initial_code = template
        return template

    # ─── Timer ───

    def _get_elapsed(self) -> float:
        elapsed = self._timer_elapsed
        if self._timer_running:
            elapsed += time.monotonic() - self._timer_start
        return elapsed

    def _update_timer_display(self):
        pid = self.problem["id"]
        elapsed = self._get_elapsed()
        best = self.progress.get(pid, {}).get("best_time")
        best_str = f"  |  Best: {fmt_duration(best)}" if best else ""
        state = "▶" if self._timer_running else "⏸"
        self.query_one("#timer-bar", Static).update(
            f" {state} Timer: {fmt_duration(elapsed)}{best_str}  [^T pause  ^R reset]"
        )

    def _tick_timer(self):
        self._update_timer_display()

    def action_toggle_timer(self):
        if self._timer_running:
            self._timer_elapsed += time.monotonic() - self._timer_start
            self._timer_running = False
            if self._timer_interval:
                self._timer_interval.stop()
                self._timer_interval = None
        else:
            self._timer_start = time.monotonic()
            self._timer_running = True
            self._timer_interval = self.set_interval(1.0, self._tick_timer)
        self._update_timer_display()

    def action_reset_timer(self):
        self._timer_elapsed = 0.0
        self._timer_start = time.monotonic()
        if not self._timer_running:
            self._timer_running = True
            self._timer_interval = self.set_interval(1.0, self._tick_timer)
        self._update_timer_display()

    def _save_timer(self):
        elapsed = self._get_elapsed()
        if elapsed > 0:
            pid = self.problem["id"]
            if pid not in self.progress:
                self.progress[pid] = {}
            best = self.progress[pid].get("best_time")
            if best is None or elapsed < best:
                self.progress[pid]["best_time"] = round(elapsed, 1)
                save_progress(self.progress)

    # ─── Actions ───

    def action_save(self):
        editor = self.query_one("#code-editor", CodeEditor)
        save_solution(self.problem["id"], self.lang, editor.text)
        self._refresh_status("✓ Saved!")

    def action_mark_done(self):
        pid = self.problem["id"]
        if pid not in self.progress:
            self.progress[pid] = {}
        self.progress[pid]["solved"] = not self.progress[pid].get("solved", False)
        if self.progress[pid]["solved"]:
            self.progress[pid]["solved_date"] = date.today().isoformat()
            self._save_timer()
        save_progress(self.progress)
        self._refresh_status()

    def action_toggle_bookmark(self):
        pid = self.problem["id"]
        if pid not in self.progress:
            self.progress[pid] = {}
        self.progress[pid]["bookmarked"] = not self.progress[pid].get("bookmarked", False)
        save_progress(self.progress)
        bm = self.progress[pid]["bookmarked"]
        bm_str = "  ★ Bookmarked" if bm else ""
        self.query_one("#problem-title", Static).update(
            f"[bold]{self.problem['name']}[/bold]{bm_str}"
        )
        self._refresh_status("★ Bookmarked!" if bm else "Bookmark removed")

    def _refresh_status(self, flash: str | None = None):
        pid = self.problem["id"]
        solved = self.progress.get(pid, {}).get("solved", False)
        marker = "✓ SOLVED" if solved else "○ UNSOLVED"
        extra = f"  {flash}  |" if flash else "  |"
        self.query_one("#status-bar", Static).update(
            f" {marker}{extra}  ^S Save  ^D Done  ^E AI  ^L Lang  ^B Bookmark  |  Esc: Back"
        )

    def action_toggle_lang(self):
        editor = self.query_one("#code-editor", CodeEditor)
        save_solution(self.problem["id"], self.lang, editor.text)
        idx = LANG_ORDER.index(self.lang)
        self.lang = LANG_ORDER[(idx + 1) % len(LANG_ORDER)]
        self.query_one("#lang-indicator", Static).update(f"  Language: {self.lang}")
        code = self._load_or_template()
        editor.text = code
        editor.language = EDITOR_LANG[self.lang]

    def action_evaluate(self):
        editor = self.query_one("#code-editor", CodeEditor)
        code = editor.text.strip()
        if not code:
            self._refresh_status("Nothing to evaluate!")
            return
        save_solution(self.problem["id"], self.lang, editor.text)
        self._refresh_status("⏳ Evaluating with AI...")
        self._run_evaluate(code)

    @work(thread=True, exclusive=True)
    def _run_evaluate(self, code: str) -> None:
        from ..ai import evaluate
        result = evaluate(self.problem, code, self.lang)
        self.app.call_from_thread(self._show_evaluate, result)

    def _show_evaluate(self, result: str) -> None:
        from .evaluate import EvaluateScreen
        self.app.push_screen(EvaluateScreen(self.problem["name"], result))
        self._refresh_status()

    def action_go_back(self):
        editor = self.query_one("#code-editor", CodeEditor)
        if editor.text.strip() and editor.text != self._initial_code:
            save_solution(self.problem["id"], self.lang, editor.text)
        self._save_timer()
        if self._timer_interval:
            self._timer_interval.stop()
        self.app.pop_screen()
