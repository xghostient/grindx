import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ListNode, linked_list_to_list, load_cases, report_ac, report_progress, report_wa


def build_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for value in values[1:]:
        cur.next = ListNode(value)
        cur = cur.next
    return head


def tail(head):
    cur = head
    while cur and cur.next:
        cur = cur.next
    return cur


def build_intersection(prefix_a, prefix_b, shared):
    shared_head = build_list(shared)
    head_a = build_list(prefix_a)
    head_b = build_list(prefix_b)
    if head_a is None:
        head_a = shared_head
    elif shared_head is not None:
        tail(head_a).next = shared_head
    if head_b is None:
        head_b = shared_head
    elif shared_head is not None:
        tail(head_b).next = shared_head
    return head_a, head_b, shared_head


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("intersection-of-two-linked-lists")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head_a, head_b, shared = build_intersection(*case["input"])
        result = mod.getIntersectionNode(head_a, head_b)
        ok = (result is shared)
        actual = linked_list_to_list(result)
        if not ok:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
