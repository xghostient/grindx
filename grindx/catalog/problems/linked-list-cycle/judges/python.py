"""Judge for Linked List Cycle — function pattern, cycle detection."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ListNode, load_cases, report_ac, report_progress, report_wa


def build_linked_list_with_cycle(values: list, pos: int) -> "ListNode | None":
    """Build a linked list from values and create a cycle at index pos.

    If pos is -1, no cycle is created. Otherwise, the tail node's next
    pointer is set to the node at index pos.
    """
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def generate_large_cases() -> list[dict]:
    """Generate max-constraint cyclic and acyclic lists."""
    values = [((k * 17) % 200001) - 100000 for k in range(10000)]
    return [
        {
            "input": [values, 5000],
            "expected": True,
            "category": "stress",
        },
        {
            "input": [values, -1],
            "expected": False,
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

    tc = load_cases("linked-list-cycle")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        values = case["input"][0]
        pos = case["input"][1]
        head = build_linked_list_with_cycle(list(values), pos)

        result = mod.hasCycle(head)

        if bool(result) != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
