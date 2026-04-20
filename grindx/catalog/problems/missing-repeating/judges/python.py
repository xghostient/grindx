"""Generated judge for missing-repeating."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import compare, load_cases, report_ac, report_progress, report_wa


def build_large_case(n: int, missing: int, repeating: int) -> dict:
    arr = list(range(1, n + 1))
    arr[missing - 1] = repeating
    return {
        "input": [arr],
        "expected": [repeating, missing],
        "category": "stress",
    }


def generate_large_cases() -> list[dict]:
    n = 100_000
    return [
        build_large_case(n, 1, n),
        build_large_case(n, n, n // 2),
        build_large_case(n, 42_424, 99_999),
    ]


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "findMissingRepeating", None)
    if fn is None:
        print("Missing function: findMissingRepeating", file=sys.stderr)
        sys.exit(2)

    tc = load_cases("missing-repeating")
    cases = tc["cases"] + generate_large_cases()
    total = len(cases)
    for i, case in enumerate(cases):
        input_values = case["input"]
        arg0 = list(input_values[0])
        result = fn(arg0)
        actual = list(result) if isinstance(result, tuple) else result
        if not compare(actual, case["expected"], "exact"):
            report_wa(i, case, actual, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
