"""grindx — Distraction-free DSA practice in your terminal."""

import argparse
import sys

from . import __version__

_HELP_TEXT = """\
grindx — Distraction-free DSA practice in your terminal

Usage:
  grindx                  Launch the TUI
  grindx --help           Show this help
  grindx --version        Show version
  grindx --list-problems  List all available problem IDs
  grindx --solved         List all solved problems
  grindx --fetch-testcases
                         Download and install an external testcase bundle
  grindx --testcase-bundle-status
                         Show installed external testcase bundle metadata

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
  Ctrl+R              Run tests
  Ctrl+Shift+R        Reset timer
  Ctrl+Shift+C/V      Copy / paste (clipboard)
  Alt+↑/↓             Move line up / down
  Alt+Shift+↓         Duplicate line

Result Screen:
  Ctrl+Y              Copy verdict + error details
  Ctrl+Shift+C        Copy verdict + error details
  r                   Retry

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
  External testcase bundles install under ~/.grindx/downloaded-testcases/
  Packaged installs do not include bundled testcases; fetch them once before local test runs.

Custom Sheets & Problems:
  Add custom sheets:   ~/.grindx/sheets/my-list.json
  Add custom problems: ~/.grindx/problems/my-problem/problem.json
  Optional local test cases: ~/.grindx/problems/my-problem/testcases.json
  Optional local judges: ~/.grindx/problems/my-problem/judges/<language>.<ext>

  Sheet format:
    {"Topic Name": ["my-problem", "another-problem"]}

  Preferred problem format:
    ~/.grindx/problems/my-problem/problem.json

  Legacy ~/.grindx/problems/custom.json is still loaded for compatibility.

  Use grindx --list-problems to see all available problem IDs.

External Testcase Bundles:
  Default manifest:
    https://github.com/grindxhq/dsa-catalog/releases/latest/download/manifest.json

  Override with:
    --testcase-manifest-url URL
  or:
    GRINDX_TESTCASE_MANIFEST_URL=https://...
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
    parser.add_argument(
        "--solved", action="store_true",
        help="List all solved problems",
    )
    parser.add_argument(
        "--fetch-testcases", action="store_true",
        help="Download and install an external testcase bundle",
    )
    parser.add_argument(
        "--testcase-bundle-status", action="store_true",
        help="Show installed external testcase bundle metadata",
    )
    parser.add_argument(
        "--testcase-manifest-url",
        help="Manifest URL used by --fetch-testcases",
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
        items = [(pid, problems[pid].get("difficulty", "")) for pid in sorted(problems)]
        w = max(len(pid) for pid, _ in items) + 2
        for pid, diff in items:
            print(f"  {pid:<{w}} {diff}")
        print(f"\n  {len(items)} problems available")
        sys.exit(0)

    if args.solved:
        from .data import load_all_problems, load_progress, fmt_duration
        problems = load_all_problems()
        progress = load_progress()
        solved = []
        for pid, pdata in progress.items():
            if pid.startswith("_"):
                continue
            if pdata.get("solved"):
                prob = problems.get(pid)
                name = prob["name"] if prob else pid
                diff = prob.get("difficulty", "") if prob else ""
                best = pdata.get("best_time")
                solved_date = pdata.get("solved_date", "")
                solved.append((name, diff, best, solved_date))
        solved.sort(key=lambda x: x[3], reverse=True)
        w = max((len(n) for n, _, _, _ in solved), default=20) + 2
        for name, diff, best, sd in solved:
            time_str = fmt_duration(best) if best and best >= 10 else ""
            print(f"  {name:<{w}} {diff:8s} {sd:12s} {time_str}")
        print(f"\n  {len(solved)} problems solved")
        sys.exit(0)

    if args.testcase_bundle_status:
        from .data import installed_testcase_bundle_metadata

        meta = installed_testcase_bundle_metadata()
        if not meta:
            print("No external testcase bundle installed")
            sys.exit(0)

        print("Installed external testcase bundle")
        for key in (
            "manifest_version",
            "bundle_format_version",
            "bundle_kind",
            "release_tag",
            "catalog_commit_short",
            "min_app_version",
            "problem_count",
            "installed_at",
            "manifest_url",
        ):
            value = meta.get(key)
            if value:
                print(f"  {key}: {value}")
        sys.exit(0)

    if args.fetch_testcases:
        from .data import fetch_testcase_bundle

        try:
            meta = fetch_testcase_bundle(args.testcase_manifest_url)
        except Exception as exc:
            print(f"Failed to install testcase bundle: {exc}", file=sys.stderr)
            sys.exit(1)

        print("Installed external testcase bundle")
        print(f"  release_tag: {meta.get('release_tag', '')}")
        print(f"  problem_count: {meta.get('problem_count', '')}")
        print(f"  sha256: {meta.get('sha256', '')}")
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
