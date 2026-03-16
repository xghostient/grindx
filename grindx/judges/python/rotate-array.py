"""Judge for Rotate Array — in-place mutation pattern."""

import importlib.util
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_wa


def generate_large_cases() -> list[dict]:
    """Generate large array for TLE detection. Deterministic via seed."""
    random.seed(42)
    cases = []
    n = 100_000
    nums = [random.randint(-(10**9), 10**9) for _ in range(n)]
    k = random.randint(1, n - 1)
    # Rotate right by k: last k elements move to front
    expected = nums[-(k % n) :] + nums[: -(k % n)]
    cases.append(
        {
            "input": [nums, k],
            "expected": expected,
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

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
