import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import ListNode, load_cases, report_ac, report_progress, report_wa


def build_cycle_list(values, pos):
    if not values:
        return None, []
    head = ListNode(values[0])
    nodes = [head]
    cur = head
    for value in values[1:]:
        cur.next = ListNode(value)
        cur = cur.next
        nodes.append(cur)
    if pos >= 0:
        cur.next = nodes[pos]
    return head, nodes


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("linked-list-cycle-ii")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head, nodes = build_cycle_list(list(case["input"][0]), case["input"][1])
        result = mod.detectCycle(head)
        expected = case["expected"]
        actual = -1
        if result is not None:
            for idx, node in enumerate(nodes):
                if result is node:
                    actual = idx
                    break
        if actual != expected:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
