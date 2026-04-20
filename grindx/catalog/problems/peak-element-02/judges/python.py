import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("peak-element-02")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        mat = [list(row) for row in case["input"][0]]
        result = mod.findPeakGrid([list(row) for row in mat])
        rows, cols = len(mat), len(mat[0])
        valid = isinstance(result, (list, tuple)) and len(result) == 2
        if valid:
            r, c = result[0], result[1]
            valid = (
                isinstance(r, int)
                and not isinstance(r, bool)
                and isinstance(c, int)
                and not isinstance(c, bool)
                and 0 <= r < rows
                and 0 <= c < cols
            )
        if valid:
            val = mat[r][c]
            if r > 0 and mat[r - 1][c] >= val:
                valid = False
            if r < rows - 1 and mat[r + 1][c] >= val:
                valid = False
            if c > 0 and mat[r][c - 1] >= val:
                valid = False
            if c < cols - 1 and mat[r][c + 1] >= val:
                valid = False
        if not valid:
            report_wa(i, case, result, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
