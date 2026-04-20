import hashlib
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from grindx import data


class TestcaseBundleFetchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)

        self.prev_user_dir = data.USER_DIR
        self.prev_user_problems_dir = data.USER_PROBLEMS_DIR
        self.prev_downloaded_testcases_dir = data.DOWNLOADED_TESTCASES_DIR
        self.prev_downloaded_bundle_meta = data.DOWNLOADED_TESTCASE_BUNDLE_META
        self.prev_catalog_problems_dir = data.CATALOG_PROBLEMS_DIR

        data.USER_DIR = root / ".grindx"
        data.USER_PROBLEMS_DIR = data.USER_DIR / "problems"
        data.DOWNLOADED_TESTCASES_DIR = data.USER_DIR / "downloaded-testcases"
        data.DOWNLOADED_TESTCASE_BUNDLE_META = data.DOWNLOADED_TESTCASES_DIR / ".bundle.json"
        data.CATALOG_PROBLEMS_DIR = root / "catalog-problems"

    def tearDown(self) -> None:
        data.USER_DIR = self.prev_user_dir
        data.USER_PROBLEMS_DIR = self.prev_user_problems_dir
        data.DOWNLOADED_TESTCASES_DIR = self.prev_downloaded_testcases_dir
        data.DOWNLOADED_TESTCASE_BUNDLE_META = self.prev_downloaded_bundle_meta
        data.CATALOG_PROBLEMS_DIR = self.prev_catalog_problems_dir
        self.tmp.cleanup()

    def _write_bundle(self, release_dir: Path, problem_id: str, payload: dict) -> Path:
        testcase_dir = release_dir / problem_id
        testcase_dir.mkdir(parents=True, exist_ok=True)
        testcase_path = testcase_dir / "testcases.json"
        testcase_path.write_text(json.dumps(payload, indent=2) + "\n")

        archive_path = release_dir / "testcases.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tf:
            tf.add(testcase_path, arcname=f"{problem_id}/testcases.json")

        sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        manifest = {
            "manifest_version": 1,
            "bundle_format_version": 1,
            "bundle_kind": "testcases-only",
            "release_tag": "testcases-vtest",
            "catalog_commit": "abc123",
            "catalog_commit_short": "abc123",
            "min_app_version": "0.2.4",
            "filename": archive_path.name,
            "sha256": sha256,
            "size_bytes": archive_path.stat().st_size,
            "problem_count": 1,
            "problems": [problem_id],
        }
        manifest_path = release_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        return manifest_path

    def test_fetch_testcase_bundle_installs_downloaded_bundle(self) -> None:
        release_dir = Path(self.tmp.name) / "release"
        manifest_path = self._write_bundle(
            release_dir,
            "alpha-problem",
            {
                "problem_id": "alpha-problem",
                "function": "solve",
                "pattern": "function",
                "comparison": "exact",
                "time_limit_s": 5,
                "cases": [{"input": [1], "expected": 2}],
            },
        )

        meta = data.fetch_testcase_bundle(manifest_path.as_uri())

        installed_testcase = (
            data.DOWNLOADED_TESTCASES_DIR / "alpha-problem" / "testcases.json"
        )
        self.assertTrue(installed_testcase.exists())
        self.assertEqual(meta["release_tag"], "testcases-vtest")
        self.assertEqual(data.testcase_path("alpha-problem"), installed_testcase)

        installed_meta = data.installed_testcase_bundle_metadata()
        self.assertIsNotNone(installed_meta)
        self.assertEqual(installed_meta["manifest_url"], manifest_path.as_uri())

    def test_user_override_testcase_wins_over_downloaded_bundle(self) -> None:
        release_dir = Path(self.tmp.name) / "release"
        manifest_path = self._write_bundle(
            release_dir,
            "shared-problem",
            {
                "problem_id": "shared-problem",
                "function": "solve",
                "pattern": "function",
                "comparison": "exact",
                "time_limit_s": 5,
                "cases": [{"input": [1], "expected": 2}],
            },
        )
        data.fetch_testcase_bundle(manifest_path.as_uri())

        user_problem_dir = data.USER_PROBLEMS_DIR / "shared-problem"
        user_problem_dir.mkdir(parents=True, exist_ok=True)
        override_path = user_problem_dir / "testcases.json"
        override_path.write_text(
            json.dumps(
                {
                    "problem_id": "shared-problem",
                    "function": "solve",
                    "pattern": "function",
                    "comparison": "exact",
                    "time_limit_s": 5,
                    "cases": [{"input": [9], "expected": 9}],
                },
                indent=2,
            )
            + "\n"
        )

        self.assertEqual(data.testcase_path("shared-problem"), override_path)

    def test_fetch_rejects_incompatible_min_app_version(self) -> None:
        release_dir = Path(self.tmp.name) / "release"
        manifest_path = self._write_bundle(
            release_dir,
            "future-problem",
            {
                "problem_id": "future-problem",
                "function": "solve",
                "pattern": "function",
                "comparison": "exact",
                "time_limit_s": 5,
                "cases": [{"input": [1], "expected": 2}],
            },
        )

        manifest = json.loads(manifest_path.read_text())
        manifest["min_app_version"] = "99.0.0"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        with self.assertRaisesRegex(ValueError, "older than required version"):
            data.fetch_testcase_bundle(manifest_path.as_uri())

        self.assertFalse(data.DOWNLOADED_TESTCASES_DIR.exists())

    def test_fetch_rejects_archive_with_unlisted_problem(self) -> None:
        release_dir = Path(self.tmp.name) / "release"
        release_dir.mkdir(parents=True, exist_ok=True)

        alpha_dir = release_dir / "alpha-problem"
        alpha_dir.mkdir(parents=True, exist_ok=True)
        (alpha_dir / "testcases.json").write_text(
            json.dumps(
                {
                    "problem_id": "alpha-problem",
                    "function": "solve",
                    "pattern": "function",
                    "comparison": "exact",
                    "time_limit_s": 5,
                    "cases": [{"input": [1], "expected": 2}],
                },
                indent=2,
            )
            + "\n"
        )

        rogue_dir = release_dir / "rogue-problem"
        rogue_dir.mkdir(parents=True, exist_ok=True)
        (rogue_dir / "testcases.json").write_text(
            json.dumps(
                {
                    "problem_id": "rogue-problem",
                    "function": "solve",
                    "pattern": "function",
                    "comparison": "exact",
                    "time_limit_s": 5,
                    "cases": [{"input": [9], "expected": 9}],
                },
                indent=2,
            )
            + "\n"
        )

        archive_path = release_dir / "testcases.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tf:
            tf.add(alpha_dir / "testcases.json", arcname="alpha-problem/testcases.json")
            tf.add(rogue_dir / "testcases.json", arcname="rogue-problem/testcases.json")

        manifest = {
            "manifest_version": 1,
            "bundle_format_version": 1,
            "bundle_kind": "testcases-only",
            "release_tag": "testcases-vtest",
            "catalog_commit": "abc123",
            "catalog_commit_short": "abc123",
            "min_app_version": "0.2.4",
            "filename": archive_path.name,
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "size_bytes": archive_path.stat().st_size,
            "problem_count": 1,
            "problems": ["alpha-problem"],
        }
        manifest_path = release_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        with self.assertRaisesRegex(ValueError, "unexpected problem ID"):
            data.fetch_testcase_bundle(manifest_path.as_uri())

    def test_manifest_resolution_falls_back_to_official_default(self) -> None:
        self.assertEqual(
            data.resolve_testcase_manifest_url(""),
            data.DEFAULT_TESTCASE_MANIFEST_URL,
        )


if __name__ == "__main__":
    unittest.main()
