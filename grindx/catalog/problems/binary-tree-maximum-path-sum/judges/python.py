import importlib.util
import os
import sys

sys.setrecursionlimit(1_000_000)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import list_to_tree, tree_to_list, load_cases, report_ac, report_progress, report_wa

def find_node(root, target):
    if root is None:
        return None
    if root.val == target:
        return root
    return find_node(root.left, target) or find_node(root.right, target)


def inorder_values(root):
    if root is None:
        return []
    return inorder_values(root.left) + [root.val] + inorder_values(root.right)


def preorder_values(root):
    if root is None:
        return []
    return [root.val] + preorder_values(root.left) + preorder_values(root.right)


def postorder_values(root):
    if root is None:
        return []
    return postorder_values(root.left) + postorder_values(root.right) + [root.val]


def level_order_values(root):
    if root is None:
        return []
    out = []
    queue = [(root, 0)]
    while queue:
        node, depth = queue.pop(0)
        if depth == len(out):
            out.append([])
        out[depth].append(node.val)
        if node.left is not None:
            queue.append((node.left, depth + 1))
        if node.right is not None:
            queue.append((node.right, depth + 1))
    return out


def is_balanced_tree(root):
    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        if left is None or right is None or abs(left - right) > 1:
            return None
        return 1 + max(left, right)
    return height(root) is not None


def run(solution_path: str) -> None:
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tc = load_cases("binary-tree-maximum-path-sum")
    cases = tc["cases"]
    total = len(cases)
    for i, case in enumerate(cases):
        root = list_to_tree(case["input"][0])
        actual = mod.maxPathSum(root)
        if actual != case["expected"]:
            report_wa(i, case, actual, total)
        report_progress(i + 1, total)
    report_ac(total)


if __name__ == "__main__":
    run(sys.argv[1])
