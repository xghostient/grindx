"""Generated judge for pascals-triangle."""

import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import compare, load_cases, report_ac, report_progress, report_wa


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    if spec is None or spec.loader is None:
        print(f"Could not load solution: {solution_path}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "generate", None)
    if fn is None:
        print("Missing function: generate", file=sys.stderr)
        sys.exit(2)

    tc = load_cases("pascals-triangle")
    total = len(tc["cases"])
    for i, case in enumerate(tc["cases"]):
        input_values = case["input"]
        arg0 = input_values[0]
        result = fn(arg0)
        actual = [list(row) if isinstance(row, tuple) else row for row in result]
        if not compare(actual, case["expected"], "exact"):
            report_wa(i, case, actual, total)

        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
