import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("shortest-common-superseq")
    cases = tc["cases"]
    total = len(cases)
    def is_subsequence(needle, haystack):
        idx = 0
        for ch in haystack:
            if idx < len(needle) and needle[idx] == ch:
                idx += 1
        return idx == len(needle)

    for i, case in enumerate(cases):
        a, b = case["input"]
        actual = mod.shortestCommonSupersequence(a, b)
        if not isinstance(actual, str):
            report_wa(i, case, actual, total)
        if len(actual) != case["expected"] or not is_subsequence(a, actual) or not is_subsequence(b, actual):
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
