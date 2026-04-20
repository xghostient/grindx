const path = require("path");
const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

class Node {
  constructor(val = 0, next = null, bottom = null) {
    this.val = val;
    this.next = next;
    this.bottom = bottom;
  }
}

function buildBottom(rows) {
  const heads = [];
  for (const row of rows) {
    if (!row.length) continue;
    const head = new Node(row[0]);
    let cur = head;
    for (let i = 1; i < row.length; i++) {
      cur.bottom = new Node(row[i]);
      cur = cur.bottom;
    }
    heads.push(head);
  }
  for (let i = 0; i + 1 < heads.length; i++) heads[i].next = heads[i + 1];
  return heads.length ? heads[0] : null;
}

function bottomRepr(head) {
  const out = [];
  const seen = new Set();
  while (head) {
    if (seen.has(head)) return [-2147483648];
    seen.add(head);
    out.push(head.val);
    head = head.bottom;
  }
  return out;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.flatten;
  const tc = loadCases("flatten-dll");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    let rows = c.input[0];
    if (rows.length === 1 && Array.isArray(rows[0]) && rows[0].length && Array.isArray(rows[0][0])) {
      rows = rows[0];
    }
    const actual = bottomRepr(fn(buildBottom(rows)));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
