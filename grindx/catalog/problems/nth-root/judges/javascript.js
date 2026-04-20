const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("nth-root");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.nthRoot(c.input[0], c.input[1]);
  if (actual !== c.expected) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
