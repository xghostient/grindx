"""Data layer — loading, saving, slug helpers."""

import json
import os
import shutil
import tempfile
import hashlib
import re
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from . import __version__

_PKG_DIR = Path(__file__).parent
CATALOG_DIR = _PKG_DIR / "catalog"
CATALOG_SHEETS_DIR = CATALOG_DIR / "sheets"
CATALOG_PROBLEMS_DIR = CATALOG_DIR / "problems"
CATALOG_JUDGE_COMMON_DIR = CATALOG_DIR / "judges" / "common"
CATALOG_TOPICS_PATH = CATALOG_DIR / "topics.json"
LEGACY_BUNDLED_SHEETS_DIR = _PKG_DIR / "sheets"
LEGACY_BUNDLED_PROBLEMS_DIR = _PKG_DIR / "problems"

USER_DIR = Path.home() / ".grindx"
PROGRESS_FILE = USER_DIR / "progress.json"
PROGRESS_BACKUP_DIR = USER_DIR / "backups"
SOLUTIONS_DIR = USER_DIR / "solutions"
USER_SHEETS_DIR = USER_DIR / "sheets"
USER_PROBLEMS_DIR = USER_DIR / "problems"
DOWNLOADED_TESTCASES_DIR = USER_DIR / "downloaded-testcases"
DOWNLOADED_TESTCASE_BUNDLE_META = DOWNLOADED_TESTCASES_DIR / ".bundle.json"
TESTCASE_MANIFEST_URL_ENV = "GRINDX_TESTCASE_MANIFEST_URL"
DEFAULT_TESTCASE_MANIFEST_URL = (
    "https://github.com/grindxhq/dsa-catalog/releases/latest/download/manifest.json"
)
SUPPORTED_TESTCASE_MANIFEST_VERSION = 1
SUPPORTED_TESTCASE_BUNDLE_FORMAT_VERSION = 1
EXPECTED_TESTCASE_BUNDLE_KIND = "testcases-only"

LANG_EXT = {"Python": ".py", "Go": ".go", "C++": ".cpp", "Java": ".java", "JavaScript": ".js"}

LANG_ORDER = ["Python", "Go", "C++", "Java", "JavaScript"]

TEMPLATE_KEY = {
    "Python": "python_template",
    "Go": "go_template",
    "C++": "cpp_template",
    "Java": "java_template",
    "JavaScript": "js_template",
}

EDITOR_LANG = {
    "Python": "python",
    "Go": "go",
    "C++": "cpp",
    "Java": "java",
    "JavaScript": "javascript",
}

LANG_DIR = {
    "Python": "python",
    "Go": "go",
    "C++": "cpp",
    "Java": "java",
    "JavaScript": "javascript",
}

_problems_cache: dict[str, dict] | None = None
_topics_cache: dict[str, dict] | None = None
REQUIRED_PERFORMANCE_FIELDS = (
    "target_time",
    "accepted_time",
    "rejected_time",
    "target_space",
    "stress_intent",
    "enforcement",
)
VALID_PERFORMANCE_ENFORCEMENT = ("strict-local", "best-effort-local")


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


def _dedupe_strings(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def normalize_performance_spec(spec: object) -> dict:
    """Normalize optional performance metadata into a stable dict shape."""
    if not isinstance(spec, dict):
        return {}

    def normalize_text(key: str) -> str:
        value = spec.get(key, "")
        return value.strip() if isinstance(value, str) else ""

    def normalize_list(key: str) -> list[str]:
        value = spec.get(key, [])
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            return []
        result = []
        for item in value:
            if not isinstance(item, str):
                continue
            item = item.strip()
            if item:
                result.append(item)
        return _dedupe_strings(result)

    def normalize_enforcement() -> str:
        value = spec.get("enforcement", "")
        if not isinstance(value, str):
            return ""
        value = value.strip().lower()
        if value in VALID_PERFORMANCE_ENFORCEMENT:
            return value
        return ""

    normalized = {
        "target_time": normalize_text("target_time"),
        "accepted_time": normalize_list("accepted_time"),
        "rejected_time": normalize_list("rejected_time"),
        "target_space": normalize_text("target_space"),
        "stress_intent": normalize_text("stress_intent"),
        "enforcement": normalize_enforcement(),
        "notes": normalize_text("notes"),
        "reference_solution_required": bool(spec.get("reference_solution_required", False)),
    }

    if normalized["target_time"] and not normalized["accepted_time"]:
        normalized["accepted_time"] = [normalized["target_time"]]

    return {key: value for key, value in normalized.items() if value not in ("", [], False)}


def normalize_problem(problem: dict) -> dict:
    """Return a shallow-normalized problem record."""
    normalized = dict(problem)
    normalized["performance"] = normalize_performance_spec(problem.get("performance"))
    return normalized


def missing_required_performance_fields(spec: object) -> list[str]:
    """Return missing required fields for a complete bundled-problem performance spec."""
    normalized = normalize_performance_spec(spec)
    missing = []
    for field in REQUIRED_PERFORMANCE_FIELDS:
        if field not in normalized:
            missing.append(field)
    return missing


def clear_catalog_caches() -> None:
    """Clear cached bundled/user catalog data."""
    global _problems_cache, _topics_cache
    _problems_cache = None
    _topics_cache = None


def _load_json_file(path: Path) -> object | None:
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _iter_legacy_problem_records(root: Path) -> list[dict]:
    records = []
    if not root.exists():
        return records
    for path in sorted(root.glob("*.json")):
        data = _load_json_file(path)
        if not isinstance(data, list):
            continue
        for problem in data:
            if not isinstance(problem, dict) or "id" not in problem:
                continue
            records.append(normalize_problem(problem))
    return records


def _iter_folder_problem_records(root: Path) -> list[dict]:
    records = []
    if not root.exists():
        return records
    for path in sorted(root.glob("*/problem.json")):
        data = _load_json_file(path)
        if not isinstance(data, dict) or "id" not in data:
            continue
        records.append(normalize_problem(data))
    return records


def _problem_dir(root: Path, problem_id: str) -> Path:
    return root / problem_id


def _problem_asset_path(root: Path, problem_id: str, filename: str) -> Path:
    return _problem_dir(root, problem_id) / filename


def _problem_judge_path(root: Path, problem_id: str, lang_dir: str) -> Path:
    ext = {"python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js", "go": ".go"}
    return _problem_dir(root, problem_id) / "judges" / f"{lang_dir}{ext.get(lang_dir, '.py')}"


def _legacy_topic_records() -> dict[str, dict]:
    topics = {}
    for path in sorted(LEGACY_BUNDLED_PROBLEMS_DIR.glob("*.json")):
        data = _load_json_file(path)
        if not isinstance(data, list):
            continue
        problem_ids = [problem["id"] for problem in data if isinstance(problem, dict) and "id" in problem]
        topics[path.stem] = {
            "id": path.stem,
            "name": name_from_slug(path.stem),
            "problem_ids": problem_ids,
        }
    return topics


# ─── Sheets ───


def list_sheets() -> list[dict]:
    """Return available sheets as [{id, name, path, count}]."""
    sheets = []
    dirs = [CATALOG_SHEETS_DIR, LEGACY_BUNDLED_SHEETS_DIR, USER_SHEETS_DIR]
    seen_ids = set()
    for d in dirs:
        if not d.exists():
            continue
        for path in sorted(d.glob("*.json")):
            if path.stem in seen_ids:
                continue
            seen_ids.add(path.stem)
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


def load_all_topics() -> dict[str, dict]:
    """Load bundled topics from canonical catalog, with legacy fallback."""
    global _topics_cache
    if _topics_cache is not None:
        return _topics_cache

    data = _load_json_file(CATALOG_TOPICS_PATH)
    topics: dict[str, dict] = {}
    if isinstance(data, list):
        for topic in data:
            if not isinstance(topic, dict) or "id" not in topic:
                continue
            topics[topic["id"]] = {
                "id": topic["id"],
                "name": topic.get("name", name_from_slug(topic["id"])),
                "problem_ids": list(topic.get("problem_ids", [])),
            }
    if not topics:
        topics = _legacy_topic_records()

    _topics_cache = topics
    return _topics_cache


# ─── Problems ───


def load_all_problems() -> dict[str, dict]:
    """Load all problems from bundled canonical catalog plus legacy/new user formats."""
    global _problems_cache
    if _problems_cache is not None:
        return _problems_cache
    _problems_cache = {}

    bundled_records = _iter_folder_problem_records(CATALOG_PROBLEMS_DIR)
    if not bundled_records:
        bundled_records = _iter_legacy_problem_records(LEGACY_BUNDLED_PROBLEMS_DIR)
    for problem in bundled_records:
        _problems_cache[problem["id"]] = problem

    for problem in _iter_legacy_problem_records(USER_PROBLEMS_DIR):
        _problems_cache[problem["id"]] = problem

    for problem in _iter_folder_problem_records(USER_PROBLEMS_DIR):
        _problems_cache[problem["id"]] = problem

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
        "performance": {},
        "python_template": f"# {pretty}\n\ndef solve():\n    pass\n",
        "go_template": f"// {pretty}\n\npackage main\n\nfunc solve() {{\n\n}}\n",
        "cpp_template": f"// {pretty}\n\n#include <bits/stdc++.h>\nusing namespace std;\n\nvoid solve() {{\n\n}}\n",
        "java_template": f"// {pretty}\n\nclass Solution {{\n    public void solve() {{\n\n    }}\n}}\n",
        "js_template": f"// {pretty}\n\nfunction solve() {{\n\n}}\n",
    }


def get_problem_performance(problem_id: str) -> dict:
    """Return normalized performance metadata for a problem."""
    return get_problem(problem_id).get("performance", {})


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
    USER_DIR.mkdir(parents=True, exist_ok=True)
    if PROGRESS_FILE.exists():
        PROGRESS_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = PROGRESS_BACKUP_DIR / f"progress_{stamp}.json"
        shutil.copy2(PROGRESS_FILE, backup)
        backups = sorted(PROGRESS_BACKUP_DIR.glob("progress_*.json"))
        for old in backups[:-10]:
            old.unlink()
    fd, tmp = tempfile.mkstemp(dir=USER_DIR, suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(progress, f, indent=2)
        os.replace(tmp, PROGRESS_FILE)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


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
    lang_dir = SOLUTIONS_DIR / LANG_DIR[lang]
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


# ─── Test Cases & Judges ───


def _safe_id(name: str) -> bool:
    """Reject IDs with path traversal or separators."""
    return ".." not in name and "/" not in name and "\\" not in name


def testcase_path(problem_id: str) -> Path | None:
    """Return path to test case JSON. User dir overrides bundled."""
    if not _safe_id(problem_id):
        return None

    candidates = [
        _problem_asset_path(USER_PROBLEMS_DIR, problem_id, "testcases.json"),
        _problem_asset_path(DOWNLOADED_TESTCASES_DIR, problem_id, "testcases.json"),
        _problem_asset_path(CATALOG_PROBLEMS_DIR, problem_id, "testcases.json"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def judge_path(problem_id: str, lang_dir: str) -> Path | None:
    """Return path to the judge file for a problem + language."""
    if not _safe_id(problem_id):
        return None

    candidates = [
        _problem_judge_path(USER_PROBLEMS_DIR, problem_id, lang_dir),
        _problem_judge_path(CATALOG_PROBLEMS_DIR, problem_id, lang_dir),
    ]
    for judge in candidates:
        if judge.exists():
            return judge
    return None


def judge_common_path(lang_dir: str) -> Path | None:
    """Return path to the shared bundled judge helper file for a language."""
    names = {
        "python": "_common.py",
        "cpp": "_common.h",
        "java": "Common.java",
        "javascript": "_common.js",
        "go": "common.go",
    }
    common = CATALOG_JUDGE_COMMON_DIR / lang_dir / names.get(lang_dir, "_common.py")
    if common.exists():
        return common
    return None


def installed_testcase_bundle_metadata() -> dict | None:
    """Return metadata for an installed downloaded testcase bundle, if present."""
    data = _load_json_file(DOWNLOADED_TESTCASE_BUNDLE_META)
    return data if isinstance(data, dict) else None


def resolve_testcase_manifest_url(manifest_url: str | None = None) -> str:
    """Resolve manifest URL from explicit input or environment."""
    url = (
        manifest_url
        or os.environ.get(TESTCASE_MANIFEST_URL_ENV, "")
        or DEFAULT_TESTCASE_MANIFEST_URL
    ).strip()
    if not url:
        raise ValueError(
            "No testcase manifest URL configured. "
            f"Pass --testcase-manifest-url or set {TESTCASE_MANIFEST_URL_ENV}."
        )
    return url


def _download_bytes(url: str) -> bytes:
    with urlopen(url) as response:
        return response.read()


def _version_key(version: str) -> tuple[int, ...]:
    parts = []
    for chunk in version.strip().split("."):
        match = re.match(r"^(\d+)", chunk)
        if not match:
            break
        parts.append(int(match.group(1)))
    return tuple(parts)


def _version_at_least(current: str, minimum: str) -> bool:
    current_key = _version_key(current)
    minimum_key = _version_key(minimum)
    if not current_key or not minimum_key:
        return False
    width = max(len(current_key), len(minimum_key))
    return current_key + (0,) * (width - len(current_key)) >= minimum_key + (0,) * (
        width - len(minimum_key)
    )


def _validate_testcase_manifest(manifest: object) -> dict:
    if not isinstance(manifest, dict):
        raise ValueError("Manifest did not decode to an object")

    manifest_version = manifest.get("manifest_version")
    if manifest_version != SUPPORTED_TESTCASE_MANIFEST_VERSION:
        raise ValueError(
            "Unsupported testcase manifest version: "
            f"{manifest_version!r} (expected {SUPPORTED_TESTCASE_MANIFEST_VERSION})"
        )

    bundle_format_version = manifest.get("bundle_format_version")
    if bundle_format_version != SUPPORTED_TESTCASE_BUNDLE_FORMAT_VERSION:
        raise ValueError(
            "Unsupported testcase bundle format version: "
            f"{bundle_format_version!r} (expected {SUPPORTED_TESTCASE_BUNDLE_FORMAT_VERSION})"
        )

    bundle_kind = manifest.get("bundle_kind", EXPECTED_TESTCASE_BUNDLE_KIND)
    if bundle_kind != EXPECTED_TESTCASE_BUNDLE_KIND:
        raise ValueError(
            f"Unsupported testcase bundle kind: {bundle_kind!r} "
            f"(expected {EXPECTED_TESTCASE_BUNDLE_KIND!r})"
        )

    min_app_version = manifest.get("min_app_version", "")
    if not isinstance(min_app_version, str) or not min_app_version.strip():
        raise ValueError("Manifest is missing a valid min_app_version")
    if not _version_at_least(__version__, min_app_version.strip()):
        raise ValueError(
            f"Installed grindx {__version__} is older than required version {min_app_version}"
        )

    filename = manifest.get("filename", "")
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Manifest is missing a valid filename")

    expected_sha = manifest.get("sha256", "")
    if not isinstance(expected_sha, str) or not expected_sha.strip():
        raise ValueError("Manifest is missing sha256")

    problems = manifest.get("problems")
    if not isinstance(problems, list) or not problems:
        raise ValueError("Manifest is missing a valid problems list")

    normalized_problem_ids = []
    seen_problem_ids = set()
    for item in problems:
        if not isinstance(item, str) or not _safe_id(item):
            raise ValueError(f"Manifest contains an invalid problem ID: {item!r}")
        if item in seen_problem_ids:
            raise ValueError(f"Manifest contains duplicate problem ID: {item}")
        seen_problem_ids.add(item)
        normalized_problem_ids.append(item)

    problem_count = manifest.get("problem_count")
    if not isinstance(problem_count, int) or problem_count != len(normalized_problem_ids):
        raise ValueError(
            "Manifest problem_count does not match the number of listed problems"
        )

    return manifest


def _archive_url_for_manifest(manifest: dict, manifest_url: str) -> str:
    filename = manifest.get("filename", "")
    if not isinstance(filename, str) or not filename:
        raise ValueError("Manifest is missing a valid filename")

    archive_url = manifest.get("archive_url", "")
    if isinstance(archive_url, str) and archive_url.strip():
        return archive_url.strip()

    base_url = manifest.get("base_url", "")
    if isinstance(base_url, str) and base_url.strip():
        return urljoin(base_url.rstrip("/") + "/", filename)

    return urljoin(manifest_url, filename)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _safe_extract_tar_gz(
    archive_path: Path,
    destination_root: Path,
    expected_problem_ids: set[str],
) -> None:
    with tarfile.open(archive_path, "r:gz") as tf:
        members = tf.getmembers()
        for member in members:
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"Unsafe archive member: {member.name}")
            if member.issym() or member.islnk():
                raise ValueError(f"Unsupported archive member type: {member.name}")
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f"Unsupported archive member type: {member.name}")
            if len(member_path.parts) != 2 or member_path.name != "testcases.json":
                raise ValueError(f"Unexpected archive layout: {member.name}")
            problem_id = member_path.parts[0]
            if problem_id not in expected_problem_ids:
                raise ValueError(f"Archive contains unexpected problem ID: {problem_id}")
        tf.extractall(destination_root)


def fetch_testcase_bundle(manifest_url: str | None = None) -> dict:
    """Download, verify, and install an external testcase bundle."""
    resolved_manifest_url = resolve_testcase_manifest_url(manifest_url)
    USER_DIR.mkdir(parents=True, exist_ok=True)

    manifest = _validate_testcase_manifest(
        json.loads(_download_bytes(resolved_manifest_url).decode("utf-8"))
    )

    archive_url = _archive_url_for_manifest(manifest, resolved_manifest_url)
    archive_payload = _download_bytes(archive_url)
    expected_sha = manifest.get("sha256", "")
    actual_sha = _sha256_bytes(archive_payload)
    if actual_sha != expected_sha:
        raise ValueError(
            f"Testcase bundle checksum mismatch: expected {expected_sha}, got {actual_sha}"
        )

    staging_parent = USER_DIR / ".tmp-testcase-bundle"
    if staging_parent.exists():
        shutil.rmtree(staging_parent)
    staging_parent.mkdir(parents=True, exist_ok=True)

    archive_path = staging_parent / "bundle.tar.gz"
    archive_path.write_bytes(archive_payload)
    extract_dir = staging_parent / "bundle"
    extract_dir.mkdir(parents=True, exist_ok=True)

    try:
        expected_problem_ids = set(manifest["problems"])
        _safe_extract_tar_gz(archive_path, extract_dir, expected_problem_ids)
        for problem_id in expected_problem_ids:
            testcase_file = _problem_asset_path(extract_dir, problem_id, "testcases.json")
            if not testcase_file.exists():
                raise ValueError(f"Archive is missing extracted testcase file for {problem_id}")

        metadata = dict(manifest)
        metadata["manifest_url"] = resolved_manifest_url
        metadata["archive_url"] = archive_url
        metadata["installed_at"] = (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        )
        (extract_dir / ".bundle.json").write_text(json.dumps(metadata, indent=2) + "\n")

        if DOWNLOADED_TESTCASES_DIR.exists():
            shutil.rmtree(DOWNLOADED_TESTCASES_DIR)
        extract_dir.rename(DOWNLOADED_TESTCASES_DIR)
    finally:
        if staging_parent.exists():
            shutil.rmtree(staging_parent, ignore_errors=True)

    return metadata


# ─── Settings (stored inside progress.json under _settings) ───


def get_preferred_lang() -> str:
    progress = load_progress()
    return progress.get("_settings", {}).get("lang", "Python")


def set_preferred_lang(lang: str, progress: dict):
    if "_settings" not in progress:
        progress["_settings"] = {}
    progress["_settings"]["lang"] = lang
    save_progress(progress)
