"""Generated judge for union-find."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa


def generate_large_cases() -> list[dict]:
    cases = []
    for variant in range(4):
        n = 100_000
        unions = [[i, i + 1] for i in range(n - 1)]
        if variant == 0:
            queries = [[0, n - 1] for _ in range(100_000)]
        elif variant == 1:
            queries = [[0, n - 1 - i] for i in range(100_000)]
        elif variant == 2:
            queries = [[i, n - 1] for i in range(100_000)]
        else:
            queries = ([[0, n // 2], [n // 3, n - 1]] * 50_000)[:100_000]
        cases.append(
            {
                "input": [n, unions, queries],
                "expected": [True] * len(queries),
                "category": "tle",
            }
        )
    return cases


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cls = getattr(mod, "UnionFind", None)
    if cls is None:
        print("Missing class: UnionFind", file=sys.stderr)
        sys.exit(2)

    tc = load_cases("union-find")
    cases = tc["cases"] + generate_large_cases()
    total = len(cases)
    for i, case in enumerate(cases):
        n, unions, queries = case["input"]
        uf = cls(n)
        for x, y in unions:
            uf.union(x, y)
        actual = [bool(uf.connected(x, y)) for x, y in queries]
        if actual != case["expected"]:
            report_wa(i, case, actual, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
