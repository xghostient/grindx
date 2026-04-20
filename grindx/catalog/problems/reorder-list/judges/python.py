"""Judge for Reorder List — in-place linked list mutation pattern."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (
    report_progress,
    linked_list_to_list,
    list_to_linked_list,
    load_cases,
    report_ac,
    report_wa,
)


def reorder_expected(vals: list) -> list:
    """Compute the expected reorder result: L0 -> Ln -> L1 -> Ln-1 -> ..."""
    if len(vals) <= 1:
        return vals
    result = []
    left, right = 0, len(vals) - 1
    while left <= right:
        result.append(vals[left])
        if left != right:
            result.append(vals[right])
        left += 1
        right -= 1
    return result


def generate_large_cases() -> list[dict]:
    """Generate large odd and even lists within the published constraints."""
    vals_even = [(k % 1000) + 1 for k in range(50000)]
    vals_odd = [((k * 7) % 1000) + 1 for k in range(49999)]
    return [
        {
            "input": [vals_even],
            "expected": reorder_expected(vals_even),
            "category": "stress",
        },
        {
            "input": [vals_odd],
            "expected": reorder_expected(vals_odd),
            "category": "stress",
        },
    ]


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("reorder-list")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arr = case["input"][0]
        head = list_to_linked_list(list(arr))

        mod.reorderList(head)
        result = linked_list_to_list(head)

        if result != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
