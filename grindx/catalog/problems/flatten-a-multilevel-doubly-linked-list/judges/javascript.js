const path = require("path");
const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

class Node {
  constructor(val = 0, prev = null, next = null, child = null) {
    this.val = val;
    this.prev = prev;
    this.next = next;
    this.child = child;
  }
}

function buildLevel(spec) {
  if (!spec.length) return null;
  let head = null;
  let prev = null;
  for (const item of spec) {
    const node = new Node(item.val);
    if (head === null) head = node;
    if (prev !== null) {
      prev.next = node;
      node.prev = prev;
    }
    if (item.child && item.child.length) {
      node.child = buildLevel(item.child);
    }
    prev = node;
  }
  return head;
}

function flattenRepr(head) {
  const out = [];
  const seen = new Set();
  let prev = null;
  while (head) {
    if (seen.has(head) || head.prev !== prev || head.child !== null) return [-2147483648];
    seen.add(head);
    out.push(head.val);
    prev = head;
    head = head.next;
  }
  return out;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.flatten;
  const tc = loadCases("flatten-a-multilevel-doubly-linked-list");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const actual = flattenRepr(fn(buildLevel(c.input[0])));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
