const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("shortest-job-first");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.sjfAvgWait(c.input[0].slice()) || 0;
  if (Math.abs(actual - c.expected) > 1e-4) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
