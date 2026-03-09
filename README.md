# grindx

Distraction-free DSA practice in your terminal. Zero network footprint.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Why grindx?

- **Zero network calls** — everything runs locally, no API hits, no tracking
- **Terminal-native** — practice DSA without leaving your terminal or opening a browser
- **Multiple sheets** — Striver A2Z (316), Blind 75, NeetCode 150, Grind 75 built-in
- **Python & Go** — switch languages on the fly with `Ctrl+L`
- **Progress tracking** — solved/in-progress/not-started states, streaks, best times
- **Bookmarks & filters** — filter by difficulty (Easy/Medium/Hard) or bookmarked problems

## Install

```bash
pip install grindx
```

Or run from source:

```bash
git clone https://github.com/xghostient/grindx.git
cd grindx
python3 -m venv .venv && source .venv/bin/activate
pip install textual tree-sitter tree-sitter-python tree-sitter-go
python app.py
```

## Usage

```bash
grindx
```

### Navigation

| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate topics / problems |
| `←` `→` | Switch between topic and problem panes |
| `Enter` | Select topic or open problem |
| `Esc` | Go back |
| `q` | Quit |

### Filters

| Key | Filter |
|-----|--------|
| `a` | All problems |
| `e` | Easy |
| `m` | Medium |
| `h` | Hard |
| `b` | Bookmarked |
| `s` | Stats dashboard |

### Solve Screen

| Key | Action |
|-----|--------|
| `Ctrl+S` | Save code |
| `Ctrl+D` | Toggle solved |
| `Ctrl+L` | Switch Python / Go |
| `Ctrl+B` | Toggle bookmark |
| `Ctrl+T` | Pause / resume timer |
| `Ctrl+R` | Reset timer |
| `Esc` | Save & go back |

## Features

**Split-pane editor** — problem description on the left, code editor with syntax highlighting on the right.

**Auto-timer** — starts when you open a problem, tracks your best solve time.

**Three-state tracking** — each problem shows as not started (○), in progress (◐), or solved (✓).

**Stats dashboard** — overall progress, per-difficulty breakdown, per-topic progress bars, current streak, and top 10 best times.

**Sheet-agnostic** — drop any JSON file into `sheets/` and it auto-appears on the welcome screen. Format:

```json
{
  "Topic Name": ["problem-name-1", "problem-name-2"],
  "Another Topic": ["problem-name-3"]
}
```

**Progress safety** — automatic backups with corruption recovery. Your progress and solutions are gitignored by default.

## Built with

- [Textual](https://github.com/Textualize/textual) — TUI framework
- [tree-sitter](https://tree-sitter.github.io/) — syntax highlighting

## License

MIT
