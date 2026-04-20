const path = require("path");
const { ListNode, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function buildCycleList(values, pos) {
  if (!values.length) return { head: null, nodes: [] };
  const head = new ListNode(values[0]);
  const nodes = [head];
  let cur = head;
  for (let i = 1; i < values.length; i++) {
    cur.next = new ListNode(values[i]);
    cur = cur.next;
    nodes.push(cur);
  }
  if (pos >= 0) {
    cur.next = nodes[pos];
  }
  return { head, nodes };
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.detectCycle;
  const tc = loadCases("linked-list-cycle-ii");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const { head, nodes } = buildCycleList([...c.input[0]], c.input[1]);
    const result = fn(head);
    let actual = -1;
    for (let idx = 0; idx < nodes.length; idx++) {
      if (result === nodes[idx]) {
        actual = idx;
        break;
      }
    }
    if (actual !== c.expected) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
