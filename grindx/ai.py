"""AI evaluation for solutions — supports Anthropic, OpenAI, Groq, Ollama."""

import json
import os
import urllib.request
import urllib.error
from pathlib import Path

from . import __version__

CONFIG_PATH = Path.home() / ".grindx.toml"

_PROVIDER_DEFAULTS = {
    "ollama": ("http://localhost:11434", "llama3"),
    "anthropic": ("https://api.anthropic.com", "claude-sonnet-4-20250514"),
    "openai": ("https://api.openai.com", "gpt-4o"),
    "groq": ("https://api.groq.com/openai", "llama-3.3-70b-versatile"),
}

_USER_AGENT = f"grindx/{__version__}"


def load_ai_config() -> dict:
    """Load AI config from ~/.grindx.toml, then override with env vars."""
    config = {"provider": "", "model": "", "api_key": "", "base_url": ""}

    if CONFIG_PATH.exists():
        _load_toml(config)

    env_map = {
        "GRINDX_AI_PROVIDER": "provider",
        "GRINDX_AI_MODEL": "model",
        "GRINDX_AI_KEY": "api_key",
        "GRINDX_AI_URL": "base_url",
    }
    for env_key, cfg_key in env_map.items():
        val = os.environ.get(env_key)
        if val:
            config[cfg_key] = val

    p = config["provider"].lower()
    if p in _PROVIDER_DEFAULTS:
        default_url, default_model = _PROVIDER_DEFAULTS[p]
        if not config["base_url"]:
            config["base_url"] = default_url
        if not config["model"]:
            config["model"] = default_model

    return config


def _load_toml(config: dict):
    """Load config from TOML file (tomllib or simple fallback)."""
    try:
        import tomllib
        with open(CONFIG_PATH, "rb") as f:
            data = tomllib.load(f)
        ai = data.get("ai", {})
        for k in config:
            if k in ai:
                config[k] = ai[k]
    except ImportError:
        _parse_toml_simple(config)


def _parse_toml_simple(config: dict):
    """Minimal parser for flat [ai] section."""
    in_ai = False
    with open(CONFIG_PATH) as f:
        for line in f:
            line = line.strip()
            if line == "[ai]":
                in_ai = True
                continue
            if line.startswith("["):
                in_ai = False
                continue
            if in_ai and "=" in line:
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key in config:
                    config[key] = val


def _build_prompt(problem: dict, code: str, lang: str) -> str:
    examples = ""
    for i, ex in enumerate(problem.get("examples", []), 1):
        examples += f"\nExample {i}:\n  Input: {ex.get('input', 'N/A')}\n  Output: {ex.get('output', 'N/A')}"

    return f"""You are a rigorous DSA solution evaluator. This is a well-known competitive programming problem. Evaluate the solution strictly.

**Problem:** {problem['name']}
**Difficulty:** {problem.get('difficulty', '?')}
**Description:** {problem.get('description', 'N/A')}
**Constraints:** {problem.get('constraints', 'N/A')}
{examples}

**Language:** {lang}
**Solution:**
```
{code}
```

You MUST respond in exactly this format with these exact headers. Do not skip any section.

The VERY FIRST line of your response MUST be exactly one of:
STATUS:PASS
STATUS:FAIL
STATUS:PARTIAL

This line is machine-parsed. Do not add anything else on this line.

## Verdict
PASS, FAIL, or PARTIAL. One word, then one-line reason.

## Failing Test Cases
If FAIL or PARTIAL, list 2-3 concrete test cases where this solution produces wrong output. Format each as:
- Input: `...`
- Expected: `...`
- Actual (from this code): `...`
- Why: one-line explanation

If PASS, write "None — solution handles all cases correctly."

## Complexity Analysis
| | This Solution | Optimal |
|---|---|---|
| Time | O(?) | O(?) |
| Space | O(?) | O(?) |

This is a classic well-known problem. You know the optimal complexity — state it confidently.
If this solution is suboptimal, say so clearly.

## Correctness Notes

### What your code does
Walk through the submitted solution step by step. Explain the approach/algorithm the user is attempting. Be specific — reference line numbers.

### What the expected approach is
Explain the correct/optimal algorithm for this well-known problem. How should it work?

### Where it diverges
If the code is wrong or suboptimal, list each issue as:
- **Line X**: `<the code on that line>` — what it does wrong and what it should do instead.

If the code is correct, say "Your implementation is correct." and note any minor style improvements (but don't nitpick).

---HINTS---

## Hints
Adapt hints based on what the user has written:

**If the solution is empty/template (no real code):**
Give generic progressive hints like LeetCode, guiding toward the right approach:
1. What pattern/technique applies to this problem?
2. What data structure would help?
3. Key insight to crack it.

**If the solution has real code but is wrong/partial:**
Acknowledge what the user got RIGHT first, then build on their existing approach:
1. "Your [specific part] is correct. Now think about..."
2. "You're using [their approach]. The issue is at [specific point]..."
3. "To fix this, consider what happens when [edge case]..."

**If PASS but suboptimal:**
"Your solution works. To optimize: think about [technique] to reduce from O(x) to O(y)."

**If PASS and optimal:**
"Your solution is optimal. No hints needed."

NEVER give the full solution. Guide, don't solve.

Keep everything concise. No fluff."""


def evaluate(problem: dict, code: str, lang: str) -> str:
    """Send solution to AI for evaluation. Blocking call."""
    config = load_ai_config()

    if not config["provider"]:
        return _no_config_msg()

    prompt = _build_prompt(problem, code, lang)
    provider = config["provider"].lower()

    if provider == "anthropic":
        return _call_anthropic(config, prompt)
    elif provider in ("openai", "ollama", "groq"):
        return _call_openai_compat(config, prompt)
    else:
        return (
            f"# Unknown provider: `{config['provider']}`\n\n"
            f"Supported: `ollama`, `anthropic`, `openai`, `groq`\n\n"
            f"Any OpenAI-compatible API works — set provider to `openai` "
            f"and configure `base_url`."
        )


def _call_anthropic(config: dict, prompt: str) -> str:
    if not config["api_key"]:
        return _missing_key_msg("anthropic", "GRINDX_AI_KEY")

    url = f"{config['base_url'].rstrip('/')}/v1/messages"
    body = json.dumps({
        "model": config["model"],
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": _USER_AGENT,
        "x-api-key": config["api_key"],
        "anthropic-version": "2023-06-01",
    })

    return _do_request(req, extractor=lambda d: d["content"][0]["text"])


def _call_openai_compat(config: dict, prompt: str) -> str:
    """Works for OpenAI, Groq, Ollama, and any OpenAI-compatible API."""
    provider = config["provider"].lower()
    if provider != "ollama" and not config["api_key"]:
        return _missing_key_msg(provider, "GRINDX_AI_KEY")

    base = config["base_url"].rstrip("/")
    url = f"{base}/v1/chat/completions"

    body = json.dumps({
        "model": config["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": _USER_AGENT,
    }
    if config["api_key"]:
        headers["Authorization"] = f"Bearer {config['api_key']}"

    req = urllib.request.Request(url, data=body, headers=headers)

    return _do_request(
        req,
        extractor=lambda d: d["choices"][0]["message"]["content"],
        timeout=120 if provider == "ollama" else 60,
    )


def _do_request(req, extractor, timeout=60) -> str:
    """Execute HTTP request with user-friendly error handling."""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        return extractor(data)
    except urllib.error.HTTPError as e:
        return _format_http_error(e)
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if "refused" in reason.lower():
            return (
                "# Connection Refused\n\n"
                "Could not connect to the AI provider.\n\n"
                "- **Ollama**: Make sure it's running (`ollama serve`)\n"
                f"- **Cloud API**: Check your `base_url` setting\n"
                f"- URL tried: `{req.full_url}`"
            )
        return f"# Connection Error\n\n{reason}"
    except TimeoutError:
        return (
            "# Request Timed Out\n\n"
            "The AI provider took too long to respond. "
            "Try again or use a faster model."
        )
    except Exception as e:
        return f"# Unexpected Error\n\n`{type(e).__name__}`: {e}"


def _format_http_error(e: urllib.error.HTTPError) -> str:
    """Parse HTTP error into a helpful message."""
    raw = ""
    try:
        raw = e.read().decode()
    except Exception:
        pass

    # Try to extract message from JSON error body
    detail = ""
    try:
        err_data = json.loads(raw)
        # OpenAI/Groq format
        if "error" in err_data:
            err_obj = err_data["error"]
            if isinstance(err_obj, dict):
                detail = err_obj.get("message", "")
            else:
                detail = str(err_obj)
        # Anthropic format
        elif "message" in err_data:
            detail = err_data["message"]
    except (json.JSONDecodeError, KeyError):
        detail = raw[:500] if raw else ""

    hints = {
        401: "Invalid or missing API key. Check your `api_key` setting.",
        403: "Access denied. Your API key may lack permissions, or the provider is blocking the request.",
        404: "Endpoint not found. Check your `base_url` and `model` settings.",
        429: "Rate limited. Wait a moment and try again.",
        500: "Server error on the provider side. Try again later.",
        503: "Service unavailable. The provider may be overloaded.",
    }

    hint = hints.get(e.code, "")
    lines = [f"# API Error ({e.code})"]
    if detail:
        lines.append(f"\n{detail}")
    if hint:
        lines.append(f"\n**Hint:** {hint}")

    return "\n".join(lines)


def _missing_key_msg(provider: str, env_var: str) -> str:
    return (
        f"# API Key Required\n\n"
        f"Provider `{provider}` needs an API key.\n\n"
        f"Set it via:\n"
        f"- **Config file** `~/.grindx.toml`:\n"
        f"  ```\n  [ai]\n  api_key = \"your-key-here\"\n  ```\n\n"
        f"- **Environment variable**:\n"
        f"  ```\n  export {env_var}=your-key-here\n  ```"
    )


def _no_config_msg() -> str:
    return """# No AI Provider Configured

Set up AI evaluation with **one environment variable** or a config file.

## Quick Start (env vars)

```
export GRINDX_AI_PROVIDER=groq
export GRINDX_AI_KEY=gsk_...
```

## Or config file (`~/.grindx.toml`)

```toml
[ai]
provider = "groq"
model = "llama-3.3-70b-versatile"
api_key = "gsk_..."
```

## Supported Providers

| Provider | Needs API Key | Default Model |
|----------|--------------|---------------|
| `ollama` | No (local) | llama3 |
| `groq` | Yes | llama-3.3-70b-versatile |
| `anthropic` | Yes | claude-sonnet-4-20250514 |
| `openai` | Yes | gpt-4o |

Any OpenAI-compatible API works — set provider to `openai` and add `base_url`."""
