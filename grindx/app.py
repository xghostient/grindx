"""grindx — Distraction-free DSA practice in your terminal."""

import argparse
import sys

from . import __version__

_HELP_TEXT = """\
grindx — Distraction-free DSA practice in your terminal

Usage:
  grindx              Launch the TUI
  grindx --help       Show this help
  grindx --version    Show version

Navigation:
  ↑/↓                 Navigate topics / problems
  ←/→                 Switch panes
  Enter               Select / open problem
  Esc                 Go back
  q                   Quit

Solve Screen:
  Ctrl+S              Save code
  Ctrl+D              Toggle solved
  Ctrl+E              AI review
  Ctrl+L              Cycle language (Python → Go → C++ → Java → JS)
  Ctrl+B              Toggle bookmark
  Ctrl+T              Pause / resume timer
  Ctrl+R              Reset timer
  Ctrl+Shift+C/V      Copy / paste (clipboard)
  Alt+↑/↓             Move line up / down
  Alt+Shift+↓         Duplicate line

Browser Filters:
  a / e / m / h / b   All / Easy / Medium / Hard / Bookmarked
  s                    Stats dashboard

AI Review (Ctrl+E):
  Configure with env vars or ~/.grindx.toml:

  Environment variables:
    GRINDX_AI_PROVIDER   ollama, groq, anthropic, or openai
    GRINDX_AI_KEY        API key (not needed for ollama)
    GRINDX_AI_MODEL      Model name (optional, sensible defaults)
    GRINDX_AI_URL        Custom base URL (optional)

  Config file (~/.grindx.toml):
    [ai]
    provider = "groq"
    api_key = "gsk_..."

  Supported providers:
    ollama       Local, free           Default: llama3
    groq         Free tier available   Default: llama-3.3-70b-versatile
    anthropic    Claude                Default: claude-sonnet-4-20250514
    openai       GPT                   Default: gpt-4o

Data:
  Progress, solutions, and backups are stored in ~/.grindx/
  Built-in sheets: Blind 75, Grind 75, NeetCode 150, Striver A2Z

Custom Sheets & Problems:
  Add custom sheets:   ~/.grindx/sheets/my-list.json
  Add custom problems: ~/.grindx/problems/custom.json

  Sheet format:
    {"Topic Name": ["my-problem", "another-problem"]}

  Problem format:
    [{"id": "my-problem", "name": "My Problem", "difficulty": "Medium",
      "description": "...", "python_template": "def solve():\\n    pass\\n"}]

  Use grindx --list-problems to see all available problem IDs.
"""


def main():
    parser = argparse.ArgumentParser(
        prog="grindx",
        description="Distraction-free DSA practice in your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    parser.add_argument(
        "-h", "--help", action="store_true",
        help="Show this help message and exit",
    )
    parser.add_argument(
        "-v", "--version", action="store_true",
        help="Show version and exit",
    )
    parser.add_argument(
        "--list-problems", action="store_true",
        help="List all available problem IDs",
    )

    args = parser.parse_args()

    if args.help:
        print(_HELP_TEXT)
        sys.exit(0)

    if args.version:
        print(f"grindx {__version__}")
        sys.exit(0)

    if args.list_problems:
        from .data import load_all_problems
        problems = load_all_problems()
        for pid in sorted(problems):
            p = problems[pid]
            diff = p.get("difficulty", "")
            print(f"  {pid:40s} {diff}")
        print(f"\n  {len(problems)} problems available")
        sys.exit(0)

    from textual.app import App
    from textual.binding import Binding
    from .screens import WelcomeScreen

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

    app = GrindxApp()
    app.run()
