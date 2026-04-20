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
        return None
    head = DLLNode(arr[0])
    cur = head
    for value in arr[1:]:
        node = DLLNode(value, None, cur)
        cur.next = node
        cur = node
    return head


def normalize_pairs(result):
    normalized = []
    for pair in result:
        normalized.append([int(pair[0]), int(pair[1])])
    return sorted(normalized)


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("pairs-in-dll")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head = list_to_dll(list(case["input"][0]))
        actual = normalize_pairs(mod.findPairs(head, case["input"][1]))
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
