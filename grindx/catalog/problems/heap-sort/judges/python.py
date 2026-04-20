import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa



def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("heap-sort")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = mod.heapSort(list(case["input"][0]))
        actual_norm = list(actual) if isinstance(actual, (list, tuple)) else actual
        if actual_norm != case["expected"]:
            report_wa(i, case, actual_norm, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
