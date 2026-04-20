import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("lis-02-print-lis")
    cases = tc["cases"]
    total = len(cases)
    def is_subsequence_list(seq, arr):
        idx = 0
        for value in arr:
            if idx < len(seq) and seq[idx] == value:
                idx += 1
        return idx == len(seq)

    for i, case in enumerate(cases):
        arr = list(case["input"][0])
        actual = mod.printLIS(arr)
        if not isinstance(actual, list):
            report_wa(i, case, actual, total)
        if len(actual) != case["expected"] or any(actual[j] >= actual[j + 1] for j in range(len(actual) - 1)) or not is_subsequence_list(actual, arr):
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
