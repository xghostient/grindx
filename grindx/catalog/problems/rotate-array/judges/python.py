"""Judge for Rotate Array — in-place mutation pattern."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


def rotate_expected(nums: list[int], k: int) -> list[int]:
    effective = k % len(nums)
    if effective == 0:
        return list(nums)
    return nums[-effective:] + nums[:-effective]


def generate_large_cases() -> list[dict]:
    """Generate deterministic constraint-valid stress cases."""
    specs = [
        (100_000, 99_999, -1_000_000_000, 37),
        (100_000, 87_500, -999_900_000, 53),
        (100_000, 75_000, -999_800_000, 61),
        (100_000, 62_500, -999_700_000, 73),
        (100_000, 50_000, -999_600_000, 79),
        (100_000, 37_500, -999_500_000, 83),
        (100_000, 25_000, -999_400_000, 89),
        (99_999, 99_998, -999_300_000, 97),
    ]
    cases = []
    for n, k, start, step in specs:
        nums = [start + (i * step) for i in range(n)]
        cases.append(
            {
                "input": [nums, k],
                "expected": rotate_expected(nums, k),
                "category": "tle",
            }
        )
    return cases


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("rotate-array")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        nums = list(case["input"][0])
        k = case["input"][1]

        mod.rotate(nums, k)

        if nums != case["expected"]:
            report_wa(i, case, nums, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
