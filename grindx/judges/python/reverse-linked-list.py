"""Judge for Reverse Linked List — function pattern, linked list I/O."""

import importlib.util
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (
    linked_list_to_list,
    list_to_linked_list,
    load_cases,
    report_ac,
    report_wa,
)


def generate_large_cases() -> list[dict]:
    """Generate large linked list for TLE detection. Deterministic via seed."""
    random.seed(42)
    vals = [random.randint(-(10**9), 10**9) for _ in range(5000)]
    return [
        {
            "input": [vals],
            "expected": vals[::-1],
            "category": "tle",
        }
    ]


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("reverse-linked-list")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arr = case["input"][0]
        head = list_to_linked_list(list(arr))

        result_head = mod.reverseList(head)
        result = linked_list_to_list(result_head)

        if result != case["expected"]:
            report_wa(i, case, result, total)

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
