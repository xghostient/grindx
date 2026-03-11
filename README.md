# grindx

Distraction-free DSA practice in your terminal. Zero network footprint.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

![grindx demo](https://raw.githubusercontent.com/xghostient/grindx/main/demo-grindx.gif)

## Why grindx?

- **Zero network calls** — everything runs locally, no tracking (optional AI review)
- **Terminal-native** — practice DSA without leaving your terminal or opening a browser
- **Multiple sheets** — Striver A2Z (316), Blind 75, NeetCode 150, Grind 75 built-in
- **5 languages** — Python, Go, C++, Java, JavaScript — switch on the fly with `Ctrl+L`
- **Progress tracking** — solved/in-progress/not-started states, streaks, best times
- **Bookmarks & filters** — filter by difficulty (Easy/Medium/Hard) or bookmarked problems

## Install

```bash
pip install grindx
```

Or with [pipx](https://pipx.pypa.io/) (recommended for CLI tools):

```bash
pipx install grindx
```

Or run from source:

```bash
git clone https://github.com/xghostient/grindx.git
cd grindx
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
grindx
```

## Usage

```bash
grindx            # CLI entry point
python -m grindx  # or as a module
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
| `Ctrl+E` | AI review |
| `Ctrl+L` | Cycle language (Python → Go → C++ → Java → JS) |
| `Ctrl+B` | Toggle bookmark |
| `Ctrl+T` | Pause / resume timer |
| `Ctrl+R` | Reset timer |
| `Ctrl+Shift+C` | Copy selection to clipboard |
| `Ctrl+Shift+V` | Paste from clipboard |
| `Alt+↑` / `Alt+↓` | Move line up / down |
| `Alt+Shift+↓` | Duplicate line |
| `Esc` | Save & go back |

## Features

**Split-pane editor** — problem description on the left, code editor with syntax highlighting on the right.

**Auto-timer** — starts when you open a problem, tracks your best solve time.

**Three-state tracking** — each problem shows as not started (○), in progress (◐), or solved (✓).

**Stats dashboard** — overall progress, per-difficulty breakdown, per-topic progress bars, current streak, and top 10 best times.

**Sheet-agnostic** — built-in sheets live inside the package (`grindx/sheets/`). Format:

```json
{
  "Topic Name": ["problem-name-1", "problem-name-2"],
  "Another Topic": ["problem-name-3"]
}
```

**Progress safety** — automatic backups with corruption recovery. Progress, solutions, and backups are stored in `~/.grindx/` so they persist across installs and upgrades.

## AI Review (optional)

Press `Ctrl+E` on the solve screen to get AI-powered feedback on your solution — correctness, edge cases, complexity analysis, and a pass/fail verdict.

### Setup

Set two environment variables:

```bash
export GRINDX_AI_PROVIDER=groq              # or ollama, anthropic, openai
export GRINDX_AI_MODEL=llama-3.3-70b-versatile  # optional, sensible defaults per provider
export GRINDX_AI_KEY=gsk_...                # not needed for ollama
export GRINDX_AI_URL=https://custom.api/v1  # optional, auto-detected per provider
```

Or create `~/.grindx.toml`:

```toml
[ai]
provider = "groq"
model = "llama-3.3-70b-versatile"
api_key = "gsk_..."
```

### Supported Providers

| Provider | API Key | Default Model | Notes |
|----------|---------|---------------|-------|
| `ollama` | No | llama3 | Local, free, no network |
| `groq` | Yes | llama-3.3-70b-versatile | Fast, free tier available |
| `anthropic` | Yes | claude-sonnet-4-20250514 | Claude |
| `openai` | Yes | gpt-4o | GPT |

Any OpenAI-compatible API works — set provider to `openai` and add `base_url`.

## Built with

- [Textual](https://github.com/Textualize/textual) — TUI framework
- [tree-sitter](https://tree-sitter.github.io/) — syntax highlighting

## License

MIT
