"""grindx — Distraction-free DSA practice in your terminal."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from textual.app import App
from textual.binding import Binding
from screens import WelcomeScreen


class GrindxApp(App):
    TITLE = "grindx"
    SUB_TITLE = "Distraction-free DSA practice"

    CSS = """
    Screen { background: $background; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())


if __name__ == "__main__":
    app = GrindxApp()
    app.run()
