import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def clone_matrix(matrix):
    return [list(row) for row in matrix]


def normalize_accounts(accounts):
    if not isinstance(accounts, list):
        return None
    out = []
    for account in accounts:
        if not isinstance(account, list) or not account:
            return None
        name = account[0]
        emails = sorted(set(account[1:]))
        out.append([name] + emails)
    return sorted(out)


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("minimum-height-trees")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = sorted(mod.findMinHeightTrees(case["input"][0], clone_matrix(case["input"][1])) or [])
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
