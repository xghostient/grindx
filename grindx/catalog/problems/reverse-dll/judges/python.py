import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


class DLLNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev


def list_to_dll(arr):
    if not arr:
        return None, []
    head = DLLNode(arr[0])
    nodes = [head]
    cur = head
    for value in arr[1:]:
        node = DLLNode(value, None, cur)
        cur.next = node
        cur = node
        nodes.append(node)
    return head, nodes


def dll_to_list(head):
    out = []
    prev = None
    seen = set()
    while head is not None:
        if id(head) in seen:
            return [-2147483648]
        seen.add(id(head))
        if head.prev is not prev:
            return [-2147483648]
        out.append(head.val)
        prev = head
        head = head.next
    return out


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("reverse-dll")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head, nodes = list_to_dll(list(case["input"][0]))
        result = mod.reverseDLL(head)
        actual = dll_to_list(result)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
