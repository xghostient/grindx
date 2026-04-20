import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

from collections import Counter

def is_valid_longest_palindrome(source, expected, actual):
    return isinstance(actual, str) and actual == actual[::-1] and actual in source and len(actual) == len(expected)

def is_valid_frequency_sort(source, actual):
    if not isinstance(actual, str):
        return False
    expected = Counter(source)
    actual_counts = Counter(actual)
    if actual_counts != expected:
        return False
    freqs = expected
    return all(freqs[actual[i - 1]] >= freqs[actual[i]] for i in range(1, len(actual)))

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("longest-palindromic-substring")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = mod.longestPalindrome(case["input"][0])
        if not is_valid_longest_palindrome(case["input"][0], case["expected"], actual):
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
