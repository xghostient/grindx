import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def normalize_int_matrix(rows):
    if rows is None:
        return []
    return sorted(sorted(int(value) for value in row) for row in rows)

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("subsets")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = normalize_int_matrix(mod.subsets(*[list(a) if isinstance(a, list) else a for a in case["input"]]) or [])
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
