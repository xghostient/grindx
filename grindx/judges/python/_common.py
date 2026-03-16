"""Shared judge utilities — data structures, comparison, verdicts."""

import json
import os
import sys
from collections import deque
from pathlib import Path

# ---------------------------------------------------------------------------
# Data structures (LeetCode standard)
# ---------------------------------------------------------------------------


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals = []
        node = self
        while node:
            vals.append(str(node.val))
            node = node.next
        return " -> ".join(vals)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


class Node:
    """Graph node for problems like Clone Graph."""

    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    def __repr__(self):
        return f"Node({self.val})"


# ---------------------------------------------------------------------------
# Serialization / Deserialization
# ---------------------------------------------------------------------------


def list_to_linked_list(arr: list) -> "ListNode | None":
    """Convert a Python list to a singly linked list."""
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head


def linked_list_to_list(head: "ListNode | None") -> list:
    """Convert a singly linked list to a Python list."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def list_to_tree(arr: list) -> "TreeNode | None":
    """Convert LeetCode-style level-order list to a binary tree."""
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    while queue and i < len(arr):
        node = queue.popleft()
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root: "TreeNode | None") -> list:
    """Convert a binary tree to LeetCode-style level-order list."""
    if root is None:
        return []
    result: list = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def adj_list_to_graph(adj_list: list[list[int]]) -> "Node | None":
    """Convert adjacency list to graph of Nodes. Returns node with val=1."""
    if not adj_list:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj_list))}
    for i, neighbors in enumerate(adj_list):
        nodes[i + 1].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def graph_to_adj_list(node: "Node | None") -> list[list[int]]:
    """Convert graph to adjacency list via BFS."""
    if node is None:
        return []
    visited: dict[int, "Node"] = {}
    queue = deque([node])
    visited[node.val] = node
    while queue:
        n = queue.popleft()
        for neighbor in n.neighbors:
            if neighbor.val not in visited:
                visited[neighbor.val] = neighbor
                queue.append(neighbor)
    max_val = max(visited.keys())
    result: list[list[int]] = []
    for i in range(1, max_val + 1):
        if i in visited:
            result.append(sorted(n.val for n in visited[i].neighbors))
        else:
            result.append([])
    return result


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------


def compare(actual, expected, mode: str, tolerance: float = 1e-5) -> bool:
    """Compare actual vs expected using the specified mode."""
    if mode == "exact":
        return actual == expected
    if mode == "unordered":
        return _sorted_safe(actual) == _sorted_safe(expected)
    if mode == "unordered_nested":
        return _sorted_nested(actual) == _sorted_nested(expected)
    if mode == "float_tolerance":
        return abs(float(actual) - float(expected)) < tolerance
    # Fallback to exact
    return actual == expected


def _sorted_safe(val):
    """Sort a list, handling mixed types gracefully."""
    if not isinstance(val, list):
        return val
    try:
        return sorted(val)
    except TypeError:
        return sorted(val, key=str)


def _sorted_nested(val):
    """Sort a list of lists by sorting each inner list, then the outer."""
    if not isinstance(val, list):
        return val
    try:
        return sorted(sorted(inner) for inner in val)
    except TypeError:
        return sorted((sorted(inner, key=str) for inner in val), key=str)


# ---------------------------------------------------------------------------
# Test case loading
# ---------------------------------------------------------------------------


def load_cases(problem_id: str) -> dict:
    """Load test cases from the JSON file in the same directory."""
    path = Path(os.path.dirname(os.path.abspath(__file__))) / f"{problem_id}.json"
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Verdict reporting
# ---------------------------------------------------------------------------


def truncate(text: str, max_len: int = 200) -> str:
    """Truncate a string for display."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def report_ac(total: int) -> None:
    """Print AC verdict and exit 0."""
    print(json.dumps({"verdict": "AC", "passed": total, "total": total}))
    sys.exit(0)


def report_wa(case_idx: int, case: dict, actual, total: int) -> None:
    """Print WA details and exit 1."""
    print(
        json.dumps(
            {
                "verdict": "WA",
                "failed_case": case_idx,
                "input_preview": truncate(str(case["input"])),
                "expected_preview": truncate(str(case.get("expected"))),
                "actual_preview": truncate(str(actual)),
                "passed": case_idx,
                "total": total,
                "category": case.get("category", ""),
            }
        )
    )
    sys.exit(1)
