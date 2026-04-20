"""Judge for Two Sum — function pattern, unordered comparison."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


def generate_large_cases() -> list[dict]:
    """Generate deterministic constraint-valid stress cases."""
    n = 10_000
    cases = []

    nums = [-500_000_000] + [
        200_000_000 + ((i * 7_919) % 700_000_000) for i in range(1, n - 1)
    ] + [123_456_789]
    cases.append(
        {
            "input": [nums, -376_543_211],
            "expected_indices": [0, n - 1],
            "category": "tle",
        }
    )

    nums = [300_000_000 + ((i * 1_237) % 600_000_000) for i in range(n)]
    dup_i, dup_j = 137, 9_862
    nums[dup_i] = 123_456_789
    nums[dup_j] = 123_456_789
    cases.append(
        {
            "input": [nums, 246_913_578],
            "expected_indices": [dup_i, dup_j],
            "category": "tle",
        }
    )

    nums = [1 + ((i * 48_271) % 999_999_998) for i in range(n)]
    low_i, high_i = 4_000, 7_000
    nums[low_i] = -1_000_000_000
    nums[high_i] = 1_000_000_000
    cases.append(
        {
            "input": [nums, 0],
            "expected_indices": [low_i, high_i],
            "category": "tle",
        }
    )

    nums = [1 + ((i * 8_191) % 999_999_999) for i in range(n)]
    zero_i, zero_j = 2_500, 7_500
    nums[zero_i] = 0
    nums[zero_j] = 0
    cases.append(
        {
            "input": [nums, 0],
            "expected_indices": [zero_i, zero_j],
            "category": "tle",
        }
    )

    return cases


def is_valid_index_pair(result: object, size: int) -> bool:
    return (
        isinstance(result, (list, tuple))
        and len(result) == 2
        and all(isinstance(idx, int) and 0 <= idx < size for idx in result)
    )


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("two-sum")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        nums, target = case["input"]
        result = mod.twoSum(list(nums), target)

        if not is_valid_index_pair(result, len(nums)):
            report_wa(i, case, result, total)

        if i < len(basic_cases):
            # Basic/edge cases — compare sorted indices
            expected = case["expected"]
            if sorted(result) != sorted(expected):
                report_wa(i, case, result, total)
        else:
            # Stress cases — require the planted unique answer.
            if sorted(result) != sorted(case["expected_indices"]):
                report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
