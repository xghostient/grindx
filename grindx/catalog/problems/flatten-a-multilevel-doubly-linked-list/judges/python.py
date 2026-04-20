import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


class Node:
    def __init__(self, val=0, prev=None, next=None, child=None):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


def build_level(spec):
    if not spec:
        return None
    head = None
    prev = None
    for item in spec:
        node = Node(item["val"])
        if head is None:
            head = node
        if prev is not None:
            prev.next = node
            node.prev = prev
        child_spec = item.get("child") or []
        if child_spec:
            node.child = build_level(child_spec)
        prev = node
    return head


def flatten_repr(head):
    out = []
    prev = None
    seen = set()
    while head is not None:
        if id(head) in seen or head.prev is not prev or head.child is not None:
            return [-2147483648]
        seen.add(id(head))
        out.append(head.val)
        prev = head
        head = head.next
    return out


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("flatten-a-multilevel-doubly-linked-list")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head = build_level(case["input"][0])
        result = mod.flatten(head)
        actual = flatten_repr(result)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
