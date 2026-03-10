"""Data layer — loading, saving, slug helpers."""

import json
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
SHEETS_DIR = BASE_DIR / "sheets"
PROBLEMS_DIR = BASE_DIR / "problems"
PROGRESS_FILE = BASE_DIR / "progress.json"
PROGRESS_BACKUP_DIR = BASE_DIR / ".backups"
SOLUTIONS_DIR = BASE_DIR / "solutions"

LANG_EXT = {"Python": ".py", "Go": ".go"}

_problems_cache: dict[str, dict] | None = None


def slug_from_name(name: str) -> str:
    return name.lower().replace(" ", "-")


def name_from_slug(slug: str) -> str:
    return slug.replace("-", " ").title()


def fmt_duration(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def short_topic(key: str) -> str:
    return key.split(" - ", 1)[-1] if " - " in key else key


# ─── Sheets ───


def list_sheets() -> list[dict]:
    """Return available sheets as [{id, name, path, count}]."""
    sheets = []
    if not SHEETS_DIR.exists():
        return sheets
    for path in sorted(SHEETS_DIR.glob("*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            total = sum(len(v) for v in data.values())
            name = path.stem.replace("-", " ").title()
            sheets.append({
                "id": path.stem,
                "name": name,
                "path": path,
                "count": total,
            })
        except (json.JSONDecodeError, OSError):
            continue
    return sheets


def load_sheet(sheet_path: Path) -> dict[str, list[str]]:
    try:
        with open(sheet_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise SystemExit(f"Cannot load {sheet_path}: {e}")


# ─── Problems ───


def load_all_problems() -> dict[str, dict]:
    """Load all problems from problems/*.json into {id: problem_dict}."""
    global _problems_cache
    if _problems_cache is not None:
        return _problems_cache
    _problems_cache = {}
    if not PROBLEMS_DIR.exists():
        return _problems_cache
    for path in PROBLEMS_DIR.glob("*.json"):
        try:
            with open(path) as f:
                for p in json.load(f):
                    _problems_cache[p["id"]] = p
        except (json.JSONDecodeError, KeyError, OSError):
            continue
    return _problems_cache


def get_problem(problem_id: str) -> dict:
    """Look up a problem by ID, fall back to stub if not found."""
    problems = load_all_problems()
    if problem_id in problems:
        return problems[problem_id]
    pretty = name_from_slug(problem_id)
    return {
        "id": problem_id,
        "name": pretty,
        "difficulty": "",
        "description": "",
        "examples": [],
        "constraints": "",
        "python_template": f"# {pretty}\n\ndef solve():\n    pass\n",
        "go_template": f"// {pretty}\n\npackage main\n\nfunc solve() {{\n\n}}\n",
    }


# ─── Progress ───


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return _recover_progress()


def save_progress(progress: dict):
    if PROGRESS_FILE.exists():
        PROGRESS_BACKUP_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = PROGRESS_BACKUP_DIR / f"progress_{stamp}.json"
        shutil.copy2(PROGRESS_FILE, backup)
        backups = sorted(PROGRESS_BACKUP_DIR.glob("progress_*.json"))
        for old in backups[:-10]:
            old.unlink()
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def _recover_progress() -> dict:
    if not PROGRESS_BACKUP_DIR.exists():
        return {}
    backups = sorted(PROGRESS_BACKUP_DIR.glob("progress_*.json"), reverse=True)
    for backup in backups:
        try:
            with open(backup) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
    return {}


# ─── Solutions ───


def get_solution_path(problem_id: str, lang: str) -> Path:
    ext = LANG_EXT[lang]
    lang_dir = SOLUTIONS_DIR / lang.lower()
    lang_dir.mkdir(parents=True, exist_ok=True)
    return lang_dir / f"{problem_id}{ext}"


def load_solution(problem_id: str, lang: str) -> str:
    path = get_solution_path(problem_id, lang)
    if path.exists():
        return path.read_text()
    return ""


def save_solution(problem_id: str, lang: str, code: str):
    path = get_solution_path(problem_id, lang)
    path.write_text(code)
