import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def clone_string_matrix(matrix):
    return [list(row) for row in matrix]

def normalize_paths(paths):
    return sorted((list(path) for path in (paths or [])), key=lambda path: tuple(path))

def validate_alien_order(words, order):
    chars = {ch for word in words for ch in word}
    if not isinstance(order, str) or len(order) != len(chars) or set(order) != chars:
        return False
    rank = {ch: idx for idx, ch in enumerate(order)}
    for a, b in zip(words, words[1:]):
        limit = min(len(a), len(b))
        i = 0
        while i < limit and a[i] == b[i]:
            i += 1
        if i == limit:
            if len(a) > len(b):
                return False
            continue
        if rank[a[i]] > rank[b[i]]:
            return False
    return True

def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("reconstruct-itinerary")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        actual = mod.findItinerary(clone_string_matrix(case["input"][0])) or []
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)

if __name__ == "__main__":
    run(sys.argv[1])
