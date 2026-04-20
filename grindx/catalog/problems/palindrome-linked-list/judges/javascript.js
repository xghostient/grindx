const path = require("path");
const { listToLinkedList, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.isPalindrome;
  const tc = loadCases("palindrome-linked-list");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const actual = fn(listToLinkedList([...c.input[0]]));
    if (actual !== c.expected) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
