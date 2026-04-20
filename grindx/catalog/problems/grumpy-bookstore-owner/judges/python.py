"""Generated judge for grumpy-bookstore-owner."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import compare, load_cases, report_ac, report_progress, report_wa


def expected(customers: list[int], grumpy: list[int], minutes: int) -> int:
    base = sum(c for c, g in zip(customers, grumpy) if g == 0)
    extra = sum(c for c, g in zip(customers[:minutes], grumpy[:minutes]) if g == 1)
    best = extra
    for i in range(minutes, len(customers)):
        if grumpy[i] == 1:
            extra += customers[i]
        if grumpy[i - minutes] == 1:
            extra -= customers[i - minutes]
        if extra > best:
            best = extra
    return base + best


def generate_large_cases() -> list[dict]:
    n = 20_000
    cases = []
    for shift in range(8):
        customers = [1000 if (i + shift) % 2 == 0 else 1 for i in range(n)]
        grumpy = [1] * n
        minutes = n // 2 + (shift % 5)
        cases.append(
            {
                "input": [customers, grumpy, minutes],
                "expected": expected(customers, grumpy, minutes),
                "category": "tle",
            }
        )
    for shift in range(8):
        customers = [((i + shift) % 9) * 111 for i in range(n)]
        grumpy = [1 if (i + shift) % 3 == 0 else 0 for i in range(n)]
        minutes = n // 2 + (shift % 7)
        cases.append(
            {
                "input": [customers, grumpy, minutes],
                "expected": expected(customers, grumpy, minutes),
                "category": "tle",
            }
        )
    for shift in range(8):
        customers = [5 if (i + shift) % 4 < 2 else 20 for i in range(n)]
        grumpy = [1 if (i + shift) % 5 else 0 for i in range(n)]
        minutes = n // 3 + (shift % 11)
        cases.append(
            {
                "input": [customers, grumpy, minutes],
                "expected": expected(customers, grumpy, minutes),
                "category": "tle",
            }
        )
    for shift in range(8):
        customers = [997 - ((i + shift) % 11) for i in range(n)]
        grumpy = [1 if (i + shift) % 2 == 0 else 0 for i in range(n)]
        minutes = n - 123 - (shift % 17)
        cases.append(
            {
                "input": [customers, grumpy, minutes],
                "expected": expected(customers, grumpy, minutes),
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

    fn = getattr(mod, "maxSatisfied", None)
    if fn is None:
        print("Missing function: maxSatisfied", file=sys.stderr)
        sys.exit(2)

    tc = load_cases("grumpy-bookstore-owner")
    cases = tc["cases"] + generate_large_cases()
    total = len(cases)
    for i, case in enumerate(cases):
        input_values = case["input"]
        arg0 = list(input_values[0])
        arg1 = list(input_values[1])
        arg2 = input_values[2]
        result = fn(arg0, arg1, arg2)
        actual = result
        if not compare(actual, case["expected"], "exact"):
            report_wa(i, case, actual, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
