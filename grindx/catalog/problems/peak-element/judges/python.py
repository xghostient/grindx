import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("peak-element")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        nums = list(case["input"][0])
        idx = mod.findPeakElement(list(nums))
        n = len(nums)
        valid = isinstance(idx, int) and not isinstance(idx, bool) and 0 <= idx < n
        if valid and idx > 0 and nums[idx] <= nums[idx - 1]:
            valid = False
        if valid and idx < n - 1 and nums[idx] <= nums[idx + 1]:
            valid = False
        if not valid:
            report_wa(i, case, idx, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
