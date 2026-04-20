"""Judge for Maximum Depth of Binary Tree — function pattern, tree input, int return."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import list_to_tree, load_cases, report_ac, report_progress, report_wa


def generate_large_cases() -> list[dict]:
    """Generate a large complete binary tree for TLE detection."""
    depth = 14  # 2^14 - 1 = 16383 nodes
    n = (1 << depth) - 1
    arr = list(range(1, n + 1))
    return [
        {
            "input": [arr],
            "expected": depth,
            "category": "tle",
        }
    ]


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tc = load_cases("maximum-depth-of-binary-tree")
    basic_cases = tc["cases"]
    large_cases = generate_large_cases()
    all_cases = basic_cases + large_cases
    total = len(all_cases)

    for i, case in enumerate(all_cases):
        arr = case["input"][0]
        root = list_to_tree(list(arr))

        result = mod.maxDepth(root)

        if result != case["expected"]:
            report_wa(i, case, result, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
