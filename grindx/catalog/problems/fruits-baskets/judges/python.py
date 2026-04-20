import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

from collections import Counter

def is_valid_min_window(source, target, expected, actual):
    if not isinstance(actual, str):
        return False
    if len(actual) != len(expected):
        return False
    if expected == "":
        return actual == ""
    if actual not in source:
        return False
    need = Counter(target)
    have = Counter(actual)
    return all(have[ch] >= count for ch, count in need.items())

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("fruits-baskets")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = mod.totalFruit(list(case["input"][0]))
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
