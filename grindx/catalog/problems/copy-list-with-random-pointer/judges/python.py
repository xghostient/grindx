import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def build_random_list(spec):
    if not spec:
        return None, []
    nodes = [Node(item[0]) for item in spec]
    for idx in range(len(nodes) - 1):
        nodes[idx].next = nodes[idx + 1]
    for idx, item in enumerate(spec):
        target = item[1]
        nodes[idx].random = None if target is None else nodes[target]
    return nodes[0], nodes


def random_repr(head):
    nodes = []
    index = {}
    cur = head
    steps = 0
    while cur is not None and steps < 100000:
        index[id(cur)] = len(nodes)
        nodes.append(cur)
        cur = cur.next
        steps += 1
    if cur is not None:
        return [[-2147483648, None]]
    out = []
    for node in nodes:
        random_idx = None if node.random is None else index.get(id(node.random))
        out.append([node.val, random_idx])
    return out


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("copy-list-with-random-pointer")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        raw = case["input"][0]
        if raw == [[]]:
            raw = []
        head, originals = build_random_list(raw)
        result = mod.copyRandomList(head)
        actual = random_repr(result)
        deep_ok = all(node not in originals for node in [] if False)
        if result is not None:
            seen = set(originals)
            cur = result
            deep_ok = True
            while cur is not None:
                if cur in seen:
                    deep_ok = False
                    break
                cur = cur.next
        if actual != case["expected"] or not deep_ok:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
