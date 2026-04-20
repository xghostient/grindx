"""Judge for LRU Cache — design class pattern."""

import importlib.util
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


class ReferenceLRU:
    """Minimal correct LRU for generating expected values in large cases."""

    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
        else:
            if len(self.cache) >= self.cap:
                self.cache.popitem(last=False)
            self.cache[key] = value


def run_large_case(cache: object, total: int, case_index: int) -> None:
    """Adversarial recency-update case within the published constraints."""
    capacity = 3000
    total_ops = 200_000
    ref = ReferenceLRU(capacity)

    for key in range(capacity):
        value = (key * 97) % 100001
        cache.put(key, value)
        ref.put(key, value)

    for step in range(total_ops - capacity):
        key = (step * 1879) % capacity
        if step % 2 == 0:
            expected = ref.get(key)
            result = cache.get(key)
            if result != expected:
                case = {
                    "input": [f"stress op {step}: get({key})"],
                    "expected": expected,
                }
                report_wa(case_index, case, result, total)
        else:
            value = ((step * 7919) + key) % 100001
            cache.put(key, value)
            ref.put(key, value)


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("lru-cache")
    basic_cases = tc["cases"]
    total = len(basic_cases) + 1

    for i, case in enumerate(basic_cases):
        capacity = case["input"][0]
        operations = case["operations"]
        op_inputs = case["op_inputs"]
        expected_vals = case["expected"]

        cache = mod.LRUCache(capacity)

        for j, op in enumerate(operations):
            if op == "put":
                cache.put(op_inputs[j][0], op_inputs[j][1])
            elif op == "get":
                result = cache.get(op_inputs[j][0])
                if expected_vals[j] is not None and result != expected_vals[j]:
                    # Build a descriptive case dict for the error report
                    err_case = {
                        "input": [f"op {j}: get({op_inputs[j][0]})"],
                        "expected": expected_vals[j],
                    }
                    report_wa(i, err_case, result, total)

        report_progress(i + 1, total)
    run_large_case(mod.LRUCache(3000), total, len(basic_cases))

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
