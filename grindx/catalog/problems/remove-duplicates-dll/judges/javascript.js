const path = require("path");
const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

class DLLNode {
  constructor(val = 0, next = null, prev = null) {
    this.val = val;
    this.next = next;
    this.prev = prev;
  }
}

function listToDll(values) {
  if (!values.length) return { head: null, nodes: [] };
  const head = new DLLNode(values[0]);
  const nodes = [head];
  let cur = head;
  for (let i = 1; i < values.length; i++) {
    const node = new DLLNode(values[i], null, cur);
    cur.next = node;
    cur = node;
    nodes.push(node);
  }
  return { head, nodes };
}

function dllToList(head) {
  const out = [];
  const seen = new Set();
  let prev = null;
  while (head) {
    if (seen.has(head) || head.prev !== prev) return [-2147483648];
    seen.add(head);
    out.push(head.val);
    prev = head;
    head = head.next;
  }
  return out;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.removeDuplicates;
  const tc = loadCases("remove-duplicates-dll");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const { head, nodes } = listToDll([...c.input[0]]);
    const actual = dllToList(fn(head));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
