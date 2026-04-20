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
  if (!values.length) return null;
  const head = new DLLNode(values[0]);
  let cur = head;
  for (let i = 1; i < values.length; i++) {
    const node = new DLLNode(values[i], null, cur);
    cur.next = node;
    cur = node;
  }
  return head;
}

function normalizePairs(result) {
  return result.map((pair) => [Number(pair[0]), Number(pair[1])]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.findPairs;
  const tc = loadCases("pairs-in-dll");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const actual = normalizePairs(fn(listToDll([...c.input[0]]), c.input[1]));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
