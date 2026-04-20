import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_cases, report_ac, report_progress, report_wa

def clone_matrix(matrix):
    return [list(row) for row in matrix]


def valid_topological_order(order, v, adj):
    if not isinstance(order, list) or len(order) != v:
        return False
    pos = {}
    for idx, node in enumerate(order):
        if not isinstance(node, int) or node < 0 or node >= v or node in pos:
            return False
        pos[node] = idx
    for node in range(v):
        if node not in pos:
            return False
        for nei in adj[node]:
            if pos[node] >= pos[nei]:
                return False
    return True


def valid_course_order(order, num_courses, prerequisites):
    if not isinstance(order, list):
        return False
    if len(order) != num_courses:
        return False
    pos = {}
    for idx, course in enumerate(order):
        if not isinstance(course, int) or course < 0 or course >= num_courses or course in pos:
            return False
        pos[course] = idx
    for course, prereq in prerequisites:
        if pos[prereq] >= pos[course]:
            return False
    return True


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("course-schedule")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        num_courses = case["input"][0]
        prerequisites = clone_matrix(case["input"][1])
        actual = mod.canFinish(num_courses, prerequisites)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
