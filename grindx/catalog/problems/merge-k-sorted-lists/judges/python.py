"""Judge for Merge K Sorted Lists — function pattern, linked list I/O."""

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
    """Generate dense and sparse max-constraint merge cases."""
    dense_lists = []
    for i in range(100):
        lst = sorted((((i * 97) + (k * 29)) % 20001) - 10000 for k in range(100))
        dense_lists.append(lst)
    dense_expected = sorted(val for lst in dense_lists for val in lst)

    singleton_lists = [[((i * 37) % 20001) - 10000] for i in range(10000)]
    singleton_expected = sorted(lst[0] for lst in singleton_lists)

    sparse_lists = [[] for _ in range(10000)]
    sparse_lists[123] = [-5, -5, 0, 3]
    sparse_lists[5000] = [-1, 2, 2]
    sparse_lists[9999] = [4]
    sparse_expected = [-5, -5, -1, 0, 2, 2, 3, 4]
    return [
        {
            "input": [dense_lists],
            "expected": dense_expected,
            "category": "stress",
        },
        {
            "input": [singleton_lists],
            "expected": singleton_expected,
            "category": "stress",
        },
        {
            "input": [sparse_lists],
            "expected": sparse_expected,
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

    tc = load_cases("merge-k-sorted-lists")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arrays = case["input"][0]
        heads = [list_to_linked_list(list(arr)) for arr in arrays]

        result_head = mod.mergeKLists(heads)
        result = linked_list_to_list(result_head)

        if result != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
