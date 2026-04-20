"""Judge for Remove Nth Node From End of List — function pattern, linked list I/O."""

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


def remove_expected(vals: list[int], n: int) -> list[int]:
    remove_idx = len(vals) - n
    return [v for i, v in enumerate(vals) if i != remove_idx]


def generate_large_cases() -> list[dict]:
    """Generate max-constraint cases with repeated values."""
    vals = [((k * 7) % 11) for k in range(30)]
    return [
        {
            "input": [vals, 30],
            "expected": remove_expected(vals, 30),
            "category": "stress",
        },
        {
            "input": [vals, 15],
            "expected": remove_expected(vals, 15),
            "category": "stress",
        },
        {
            "input": [vals, 1],
            "expected": remove_expected(vals, 1),
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

    tc = load_cases("remove-nth-node-from-end-of-list")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arr = case["input"][0]
        n = case["input"][1]
        head = list_to_linked_list(list(arr))

        result_head = mod.removeNthFromEnd(head, n)
        result = linked_list_to_list(result_head)

        if result != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
