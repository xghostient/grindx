import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


class Node:
    def __init__(self, val=0, next=None, bottom=None):
        self.val = val
        self.next = next
        self.bottom = bottom


def build_bottom(rows):
    heads = []
    for row in rows:
        if not row:
            continue
        head = Node(row[0])
        cur = head
        for value in row[1:]:
            cur.bottom = Node(value)
            cur = cur.bottom
        heads.append(head)
    for left, right in zip(heads, heads[1:]):
        left.next = right
    return heads[0] if heads else None


def bottom_repr(head):
    out = []
    seen = set()
    while head is not None:
        if id(head) in seen:
            return [-2147483648]
        seen.add(id(head))
        out.append(head.val)
        head = head.bottom
    return out


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("flatten-dll")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        rows = case["input"][0]
        if rows and isinstance(rows[0], list) and len(rows) == 1 and rows[0] and isinstance(rows[0][0], list):
            rows = rows[0]
        head = build_bottom(rows)
        result = mod.flatten(head)
        actual = bottom_repr(result)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
