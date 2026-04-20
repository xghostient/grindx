"""Judge for Merge Two Sorted Lists — function pattern, linked list I/O."""

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


def generate_large_cases() -> list[dict]:
    """Generate max-constraint correctness cases within the published bounds."""
    list2_only = sorted((((k * 7) + 3) % 201) - 100 for k in range(50))
    list1 = sorted((((k * 9) + 1) % 201) - 100 for k in range(25))
    list2 = sorted((((k * 11) + 5) % 201) - 100 for k in range(25))
    return [
        {
            "input": [[], list2_only],
            "expected": list2_only,
            "category": "stress",
        },
        {
            "input": [list1, list2],
            "expected": sorted(list1 + list2),
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

    tc = load_cases("merge-two-sorted-lists")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arr1 = case["input"][0]
        arr2 = case["input"][1]
        head1 = list_to_linked_list(list(arr1))
        head2 = list_to_linked_list(list(arr2))

        result_head = mod.mergeTwoLists(head1, head2)
        result = linked_list_to_list(result_head)

        if result != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
