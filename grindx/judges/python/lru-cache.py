"""Judge for LRU Cache — design class pattern."""

import importlib.util
import os
import random
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_wa


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


def generate_large_cases() -> list[dict]:
    """Generate 200K-operation case for TLE detection. Deterministic via seed."""
    random.seed(42)
    capacity = 1000
    num_ops = 200_000

    ref = ReferenceLRU(capacity)
    operations: list[str] = []
    op_inputs: list[list[int]] = []
    expected: list[int | None] = []

    for _ in range(num_ops):
        # Bias toward put: 0 = get, 1 or 2 = put
        if random.randint(0, 2) == 0:
            key = random.randint(1, 5000)
            result = ref.get(key)
            operations.append("get")
            op_inputs.append([key])
            expected.append(result)
        else:
            key = random.randint(1, 5000)
            value = random.randint(1, 100_000)
            ref.put(key, value)
            operations.append("put")
            op_inputs.append([key, value])
            expected.append(None)

    return [
        {
            "input": [capacity],
            "operations": operations,
            "op_inputs": op_inputs,
            "expected": expected,
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

    tc = load_cases("lru-cache")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
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

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
