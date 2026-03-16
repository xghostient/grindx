"""Judge for Two Sum — function pattern, unordered comparison."""

import importlib.util
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_wa


def generate_large_cases() -> list[dict]:
    """Generate large inputs for TLE detection. Deterministic via seed."""
    random.seed(42)
    cases = []
    for n in [10_000, 100_000]:
        nums = [random.randint(-(10**9), 10**9) for _ in range(n)]
        i, j = random.sample(range(n), 2)
        target = nums[i] + nums[j]
        cases.append(
            {
                "input": [nums, target],
                "expected_indices": [i, j],
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

    tc = load_cases("two-sum")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        nums, target = case["input"]
        result = mod.twoSum(list(nums), target)

        if i < len(basic_cases):
            # Basic/edge cases — compare sorted indices
            expected = case["expected"]
            if sorted(result) != sorted(expected):
                report_wa(i, case, result, total)
        else:
            # Large cases — validate answer correctness
            if (
                not isinstance(result, (list, tuple))
                or len(result) != 2
                or result[0] == result[1]
                or nums[result[0]] + nums[result[1]] != target
            ):
                report_wa(i, case, result, total)

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
