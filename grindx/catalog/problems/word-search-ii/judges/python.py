import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("word-search-ii")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        board = [row[:] for row in case["input"][0]]
        words = list(case["input"][1])
        result = mod.findWords(board, words)
        actual = sorted(result) if isinstance(result, (list, tuple)) else result
        expected = sorted(case["expected"]) if isinstance(case["expected"], (list, tuple)) else case["expected"]
        if actual != expected:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
