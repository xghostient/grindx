import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("disjoint-set-implementation")
    cases = tc["cases"]
    total = len(cases)

    for i, case in enumerate(cases):
        dsu = mod.DSU(case["input"][0])
        for j, op in enumerate(case["operations"]):
            args = case["op_inputs"][j]
            expected = case["expected"][j]
            if op == "union":
                actual = dsu.union(args[0], args[1])
            else:
                actual = dsu.find(args[0]) == dsu.find(args[1])
            if actual != expected:
                err_case = {
                    "input": [f"op {j}: {op}{tuple(args)}"],
                    "expected": expected,
                }
                report_wa(i, err_case, actual, total)
        report_progress(i + 1, total)

    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
