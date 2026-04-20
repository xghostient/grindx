import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("lis-03-largest-div-subset")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        arr = list(case["input"][0])
        actual = mod.largestDivisibleSubset(arr)
        if not isinstance(actual, list):
            report_wa(i, case, actual, total)
        valid = len(actual) == case["expected"] and len(actual) == len(set(actual)) and all(x in arr for x in actual)
        if valid:
            for x in actual:
                for y in actual:
                    if x != y and x % y != 0 and y % x != 0:
                        valid = False
                        break
                if not valid:
                    break
        if not valid:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
