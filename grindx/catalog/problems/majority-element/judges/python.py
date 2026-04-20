"""Generated judge for majority-element."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import compare, load_cases, report_ac, report_progress, report_wa


def generate_large_cases() -> list[dict]:
    prefix = list(range(2, 25001))
    stress_one = prefix + [1] * 25001
    stress_two = [-(i + 2) for i in range(24999)] + [-1] * 25001
    stress_three = [1000000000 - i for i in range(24999)] + [999999999] * 25001
    stress_four = [-(1000000000 - i) for i in range(24999)] + [-999999999] * 25001
    stress_five = [500000000 + i for i in range(24999)] + [7] * 25001
    stress_six = [-(500000000 + i) for i in range(24999)] + [-7] * 25001
    stress_seven = [250000000 + i for i in range(24999)] + [123456789] * 25001
    stress_eight = [-(250000000 + i) for i in range(24999)] + [-123456789] * 25001
    cases = [
        {
            "input": [stress_one],
            "expected": 1,
            "category": "stress",
        },
        {
            "input": [stress_two],
            "expected": -1,
            "category": "stress",
        },
        {
            "input": [stress_three],
            "expected": 999999999,
            "category": "stress",
        },
        {
            "input": [stress_four],
            "expected": -999999999,
            "category": "stress",
        },
        {
            "input": [stress_five],
            "expected": 7,
            "category": "stress",
        },
        {
            "input": [stress_six],
            "expected": -7,
            "category": "stress",
        },
        {
            "input": [stress_seven],
            "expected": 123456789,
            "category": "stress",
        },
        {
            "input": [stress_eight],
            "expected": -123456789,
            "category": "stress",
        },
    ]
    return cases * 4


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "majorityElement", None)
    if fn is None:
        print("Missing function: majorityElement", file=sys.stderr)
        sys.exit(2)

    tc = load_cases("majority-element")
    cases = tc["cases"] + generate_large_cases()
    total = len(cases)
    for i, case in enumerate(cases):
        input_values = case["input"]
        arg0 = list(input_values[0])
        result = fn(arg0)
        actual = result
        if not compare(actual, case["expected"], "exact"):
            report_wa(i, case, actual, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
