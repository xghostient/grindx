import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import linked_list_to_list, list_to_linked_list, load_cases, report_ac, report_progress, report_wa


def generate_large_cases() -> list[dict]:
    descending = list(range(50000, 0, -1))
    descending_expected = list(range(1, 50001))

    mixed = [((i * 8191) % 200001) - 100000 for i in range(50000)]
    mixed_expected = sorted(mixed)

    duplicates = [((i * 37) % 31) - 15 for i in range(50000)]
    duplicates_expected = sorted(duplicates)

    return [
        {"input": [descending], "expected": descending_expected, "category": "stress"},
        {"input": [mixed], "expected": mixed_expected, "category": "stress"},
        {"input": [duplicates], "expected": duplicates_expected, "category": "stress"},
    ]


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("sort-list")
    cases = tc["cases"] + generate_large_cases()
    total = len(cases)
    for i, case in enumerate(cases):
        head = list_to_linked_list(list(case["input"][0]))
        result = mod.sortList(head)
        actual = linked_list_to_list(result)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
