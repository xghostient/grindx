import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def normalize_int_matrix(rows):
    if rows is None:
        return []
    return sorted(sorted(int(value) for value in row) for row in rows)

def sorted_int_list(values):
    if values is None:
        return []
    return sorted(int(value) for value in values)

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("top-k-frequent-elements")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = sorted_int_list(mod.topKFrequent(list(case["input"][0]), case["input"][1]))
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
