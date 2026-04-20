import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import linked_list_to_list, list_to_linked_list, load_cases, report_ac, report_progress, report_wa


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("insert-gcd-in-linked-list")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        head = list_to_linked_list(list(case["input"][0]))
        result = mod.insertGreatestCommonDivisors(head)
        actual = linked_list_to_list(result)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
