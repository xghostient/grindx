import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("merge-sorted-array")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        nums1 = list(case["input"][0])
        nums2 = list(case["input"][2])
        mod.merge(nums1, case["input"][1], nums2, case["input"][3])
        if nums1 != case["expected"]:
            report_wa(i, case, nums1, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
