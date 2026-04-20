import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def clone_matrix(matrix):
    return [list(row) for row in matrix]

def clone_weighted_adj(adj):
    return [[list(edge) for edge in row] for row in adj]

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("shortest-path-ug")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = mod.shortestPath(case["input"][0], clone_matrix(case["input"][1]), case["input"][2])
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == '__main__':
    run(sys.argv[1])
