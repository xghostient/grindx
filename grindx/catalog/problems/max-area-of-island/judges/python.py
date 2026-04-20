import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import adj_list_to_graph, graph_to_adj_list, load_cases, report_ac, report_progress, report_wa

def clone_matrix(matrix):
    return [list(row) for row in matrix]


def string_rows_to_grid(rows):
    return [list(row) for row in rows]


def grid_to_string_rows(grid):
    return ["".join(row) for row in grid]


def normalize_pairs(values):
    return sorted([list(pair) for pair in values])


def graph_shares_identity(original, clone):
    if original is None or clone is None:
        return False
    original_ids = set()
    queue = [original]
    while queue:
        node = queue.pop()
        node_id = id(node)
        if node_id in original_ids:
            continue
        original_ids.add(node_id)
        queue.extend(getattr(node, "neighbors", []) or [])
    queue = [clone]
    seen = set()
    while queue:
        node = queue.pop()
        node_id = id(node)
        if node_id in seen:
            continue
        if node_id in original_ids:
            return True
        seen.add(node_id)
        queue.extend(getattr(node, "neighbors", []) or [])
    return False


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("max-area-of-island")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        grid = clone_matrix(case["input"][0])
        actual = mod.maxAreaOfIsland(grid)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
