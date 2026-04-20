import json
import tempfile
import tomllib
import unittest
from pathlib import Path

from grindx import data


class CatalogMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.prev_user_problems_dir = data.USER_PROBLEMS_DIR
        self.prev_user_sheets_dir = data.USER_SHEETS_DIR
        self.prev_downloaded_testcases_dir = data.DOWNLOADED_TESTCASES_DIR
        self.prev_downloaded_bundle_meta = data.DOWNLOADED_TESTCASE_BUNDLE_META
        root = Path(self.tmp.name)
        data.USER_PROBLEMS_DIR = root / "problems"
        data.USER_SHEETS_DIR = root / "sheets"
        data.DOWNLOADED_TESTCASES_DIR = root / "downloaded-testcases"
        data.DOWNLOADED_TESTCASE_BUNDLE_META = data.DOWNLOADED_TESTCASES_DIR / ".bundle.json"
        data.clear_catalog_caches()

    def tearDown(self) -> None:
        data.USER_PROBLEMS_DIR = self.prev_user_problems_dir
        data.USER_SHEETS_DIR = self.prev_user_sheets_dir
        data.DOWNLOADED_TESTCASES_DIR = self.prev_downloaded_testcases_dir
        data.DOWNLOADED_TESTCASE_BUNDLE_META = self.prev_downloaded_bundle_meta
        data.clear_catalog_caches()
        self.tmp.cleanup()

    def test_bundled_catalog_problem_and_judge_resolve_from_new_layout(self) -> None:
        problem = data.get_problem("two-sum")
        testcase = data.testcase_path("two-sum")
        judge = data.judge_path("two-sum", "python")
        common = data.judge_common_path("python")

        self.assertEqual(problem["id"], "two-sum")
        self.assertIsNone(testcase)
        self.assertIsNotNone(judge)
        self.assertEqual(
            judge,
            data.CATALOG_PROBLEMS_DIR / "two-sum" / "judges" / "python.py",
        )
        self.assertEqual(
            common,
            data.CATALOG_JUDGE_COMMON_DIR / "python" / "_common.py",
        )
        self.assertTrue((data.CATALOG_PROBLEMS_DIR / "two-sum" / "problem.json").exists())
        self.assertTrue((data.CATALOG_PROBLEMS_DIR / "two-sum" / "judges" / "python.py").exists())
        self.assertFalse((data.CATALOG_PROBLEMS_DIR / "two-sum" / "testcases.json").exists())
        self.assertTrue((data.CATALOG_JUDGE_COMMON_DIR / "python" / "_common.py").exists())

    def test_topics_load_from_canonical_catalog(self) -> None:
        topics = data.load_all_topics()
        self.assertIn("arrays", topics)
        self.assertIn("two-sum", topics["arrays"]["problem_ids"])
        self.assertIn("linked-list", topics)
        self.assertIn("reverse-linked-list", topics["linked-list"]["problem_ids"])

    def test_legacy_custom_problem_file_still_loads(self) -> None:
        data.USER_PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
        legacy_path = data.USER_PROBLEMS_DIR / "custom.json"
        legacy_path.write_text(
            json.dumps(
                [
                    {
                        "id": "legacy-custom-problem",
                        "name": "Legacy Custom Problem",
                        "difficulty": "Easy",
                    }
                ]
            )
            + "\n"
        )

        data.clear_catalog_caches()
        problem = data.get_problem("legacy-custom-problem")
        self.assertEqual(problem["name"], "Legacy Custom Problem")
        self.assertEqual(problem["performance"], {})

    def test_new_style_custom_problem_folder_overrides_legacy_file(self) -> None:
        data.USER_PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)
        (data.USER_PROBLEMS_DIR / "custom.json").write_text(
            json.dumps(
                [
                    {
                        "id": "shared-problem",
                        "name": "Legacy Name",
                        "difficulty": "Easy",
                    }
                ]
            )
            + "\n"
        )

        new_problem_dir = data.USER_PROBLEMS_DIR / "shared-problem"
        new_problem_dir.mkdir(parents=True, exist_ok=True)
        (new_problem_dir / "problem.json").write_text(
            json.dumps(
                {
                    "id": "shared-problem",
                    "name": "New Folder Name",
                    "difficulty": "Medium",
                    "performance": {"target_time": "O(n)"},
                },
                indent=2,
            )
            + "\n"
        )
        (new_problem_dir / "testcases.json").write_text(
            json.dumps(
                {
                    "problem_id": "shared-problem",
                    "function": "solve",
                    "pattern": "function",
                    "comparison": "exact",
                    "time_limit_s": 5,
                    "cases": [],
                },
                indent=2,
            )
            + "\n"
        )

        data.clear_catalog_caches()
        problem = data.get_problem("shared-problem")
        self.assertEqual(problem["name"], "New Folder Name")
        self.assertEqual(problem["performance"]["target_time"], "O(n)")
        self.assertEqual(
            data.testcase_path("shared-problem"),
            new_problem_dir / "testcases.json",
        )

    def test_new_style_custom_problem_folder_can_provide_local_judge(self) -> None:
        problem_dir = data.USER_PROBLEMS_DIR / "judge-backed-problem"
        judges_dir = problem_dir / "judges"
        judges_dir.mkdir(parents=True, exist_ok=True)
        (problem_dir / "problem.json").write_text(
            json.dumps(
                {
                    "id": "judge-backed-problem",
                    "name": "Judge Backed Problem",
                    "difficulty": "Easy",
                },
                indent=2,
            )
            + "\n"
        )
        (judges_dir / "python.py").write_text("# custom judge\n")

        data.clear_catalog_caches()
        self.assertEqual(
            data.judge_path("judge-backed-problem", "python"),
            judges_dir / "python.py",
        )

    def test_legacy_custom_sheet_format_still_lists(self) -> None:
        data.USER_SHEETS_DIR.mkdir(parents=True, exist_ok=True)
        sheet_path = data.USER_SHEETS_DIR / "custom-sheet.json"
        sheet_path.write_text(json.dumps({"Custom Topic": ["two-sum"]}, indent=2) + "\n")

        sheets = data.list_sheets()
        custom = next(sheet for sheet in sheets if sheet["id"] == "custom-sheet")
        self.assertEqual(custom["count"], 1)

    def test_package_data_no_longer_ships_bundled_testcases(self) -> None:
        pyproject = tomllib.loads(Path("pyproject.toml").read_text())
        package_data = pyproject["tool"]["setuptools"]["package-data"]["grindx"]
        self.assertNotIn("catalog/problems/*/testcases.json", package_data)


if __name__ == "__main__":
    unittest.main()
