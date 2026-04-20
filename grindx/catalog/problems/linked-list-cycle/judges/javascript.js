/**
 * Judge for Linked List Cycle — function pattern, boolean result.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  ListNode, reportProgress
} = require("./_common");

function buildCycleList(values, pos) {
  if (!values || values.length === 0) return null;
  const head = new ListNode(values[0]);
  let curr = head;
  const nodes = [head];
  for (let i = 1; i < values.length; i++) {
    curr.next = new ListNode(values[i]);
    curr = curr.next;
    nodes.push(curr);
  }
  if (pos >= 0 && pos < nodes.length) {
    curr.next = nodes[pos];
  }
  return head;
}

function generateLargeCases() {
  const cases = [];
  const values = [];
  for (let k = 0; k < 10000; k++) values.push(((k * 17) % 200001) - 100000);
  cases.push({ input: [values, 5000], expected: true, category: "stress" });
  cases.push({ input: [values, -1], expected: false, category: "stress" });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const hasCycle = sol.hasCycle;
  if (typeof hasCycle !== "function") {
    process.stderr.write("Solution does not export a hasCycle function\n");
    process.exit(2);
  }

  const tc = loadCases("linked-list-cycle");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const values = c.input[0];
    const pos = c.input[1];
    const head = buildCycleList([...values], pos);
    const result = hasCycle(head);
    const expected = c.expected;

    if (result !== expected) {
      reportWa(i, c, result, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
