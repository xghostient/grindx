/**
 * Shared judge utilities for JavaScript judges.
 */

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Data structures
// ---------------------------------------------------------------------------

class ListNode {
  constructor(val = 0, next = null) {
    this.val = val;
    this.next = next;
  }
}

class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function listToLinkedList(arr) {
  if (!arr || arr.length === 0) return null;
  const head = new ListNode(arr[0]);
  let curr = head;
  for (let i = 1; i < arr.length; i++) {
    curr.next = new ListNode(arr[i]);
    curr = curr.next;
  }
  return head;
}

function linkedListToList(head) {
  const result = [];
  const seen = new Set();
  let steps = 0;
  const maxNodes = 100000;
  while (head && steps < maxNodes) {
    if (seen.has(head)) {
      result.push(-2147483648);
      break;
    }
    seen.add(head);
    result.push(head.val);
    head = head.next;
    steps++;
  }
  if (head && steps >= maxNodes) {
    result.push(-2147483648);
  }
  return result;
}

function listToTree(arr) {
  if (!arr || arr.length === 0 || arr[0] === null) return null;
  const root = new TreeNode(arr[0]);
  const queue = [root];
  let i = 1;
  while (queue.length > 0 && i < arr.length) {
    const node = queue.shift();
    if (i < arr.length && arr[i] !== null) {
      node.left = new TreeNode(arr[i]);
      queue.push(node.left);
    }
    i++;
    if (i < arr.length && arr[i] !== null) {
      node.right = new TreeNode(arr[i]);
      queue.push(node.right);
    }
    i++;
  }
  return root;
}

class Node {
  constructor(val = 0, neighbors = [], next = null, random = null, prev = null, child = null, bottom = null) {
    this.val = val;
    this.neighbors = neighbors;
    this.next = next;
    this.random = random;
    this.prev = prev;
    this.child = child;
    this.bottom = bottom;
  }
}

function adjListToGraph(adjList) {
  if (!adjList || adjList.length === 0) return null;
  const nodes = {};
  for (let i = 0; i < adjList.length; i++) {
    nodes[i + 1] = new Node(i + 1);
  }
  for (let i = 0; i < adjList.length; i++) {
    nodes[i + 1].neighbors = adjList[i].map((n) => nodes[n]);
  }
  return nodes[1];
}

function graphToAdjList(node) {
  if (!node) return [];
  const visited = {};
  const queue = [node];
  visited[node.val] = node;
  while (queue.length > 0) {
    const n = queue.shift();
    for (const neighbor of n.neighbors) {
      if (!(neighbor.val in visited)) {
        visited[neighbor.val] = neighbor;
        queue.push(neighbor);
      }
    }
  }
  const maxVal = Math.max(...Object.keys(visited).map(Number));
  const result = [];
  for (let i = 1; i <= maxVal; i++) {
    if (visited[i]) {
      result.push(visited[i].neighbors.map((n) => n.val).sort((a, b) => a - b));
    } else {
      result.push([]);
    }
  }
  return result;
}

function treeToList(root) {
  if (!root) return [];
  const result = [];
  const queue = [root];
  while (queue.length > 0) {
    const node = queue.shift();
    if (node === null) {
      result.push(null);
    } else {
      result.push(node.val);
      queue.push(node.left);
      queue.push(node.right);
    }
  }
  while (result.length > 0 && result[result.length - 1] === null) result.pop();
  return result;
}

// ---------------------------------------------------------------------------
// Comparison
// ---------------------------------------------------------------------------

function compare(actual, expected, mode) {
  if (mode === "exact") return JSON.stringify(actual) === JSON.stringify(expected);
  if (mode === "unordered") {
    return JSON.stringify([...actual].sort((a, b) => a - b)) ===
           JSON.stringify([...expected].sort((a, b) => a - b));
  }
  if (mode === "unordered_nested") {
    const sortNested = (arr) =>
      arr.map((inner) => [...inner].sort((a, b) => a - b))
         .sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
    return JSON.stringify(sortNested(actual)) === JSON.stringify(sortNested(expected));
  }
  if (mode === "float_tolerance") {
    return Math.abs(actual - expected) < 1e-5;
  }
  return JSON.stringify(actual) === JSON.stringify(expected);
}

// ---------------------------------------------------------------------------
// Test case loading
// ---------------------------------------------------------------------------

function loadCases(problemId) {
  const p = path.join(__dirname, `${problemId}.json`);
  return JSON.parse(fs.readFileSync(p, "utf-8"));
}

// ---------------------------------------------------------------------------
// Verdict reporting
// ---------------------------------------------------------------------------

function truncate(text, maxLen = 200) {
  text = String(text);
  if (text.length <= maxLen) return text;
  return text.substring(0, maxLen - 3) + "...";
}

let progressFd = null;

function reportProgress(passed, total) {
  const progressPath = process.env.GRINDX_PROGRESS_FILE;
  if (!progressPath) return;
  try {
    if (progressFd === null) {
      progressFd = fs.openSync(progressPath, "w");
    }
    const payload = `${passed},${total}`;
    fs.ftruncateSync(progressFd, 0);
    fs.writeSync(progressFd, payload, 0, "utf8");
  } catch (_) {
    // Ignore progress persistence failures; they should not affect verdicts.
  }
}

function reportAc(total) {
  console.log(JSON.stringify({ verdict: "AC", passed: total, total }));
  process.exit(0);
}

function reportWa(caseIdx, testCase, actual, total) {
  console.log(JSON.stringify({
    verdict: "WA",
    failed_case: caseIdx,
    input_preview: truncate(JSON.stringify(testCase.input)),
    expected_preview: truncate(JSON.stringify(testCase.expected)),
    actual_preview: truncate(JSON.stringify(actual)),
    passed: caseIdx,
    total,
    category: testCase.category || "",
  }));
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Solution loading
// ---------------------------------------------------------------------------

function loadSolution(solutionPath) {
  const code = fs.readFileSync(solutionPath, "utf-8");
  const vm = require("vm");
  const sandbox = { module: { exports: {} }, exports: {}, require };
  vm.runInNewContext(code, sandbox);
  // Support both `var twoSum = function(...)` and `module.exports = { twoSum }`
  const mod = sandbox.module.exports;
  if (typeof mod === "object" && Object.keys(mod).length > 0) return mod;
  // Fall back to sandbox globals
  return sandbox;
}

module.exports = {
  ListNode, TreeNode, Node,
  listToLinkedList, linkedListToList,
  listToTree, treeToList,
  adjListToGraph, graphToAdjList,
  compare, loadCases,
  reportAc, reportProgress, reportWa, truncate,
  loadSolution,
};
