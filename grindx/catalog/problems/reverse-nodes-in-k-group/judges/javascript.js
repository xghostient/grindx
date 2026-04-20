const path = require("path");
const { listToLinkedList, linkedListToList, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.reverseKGroup;
  const tc = loadCases("reverse-nodes-in-k-group");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const head = listToLinkedList([...c.input[0]]);
    const actual = linkedListToList(fn(head, c.input[1]));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
