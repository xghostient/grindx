const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("pow-x-n");
const cases = tc.cases;
const total = cases.length;


for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.myPow(c.input[0], c.input[1]);
  if (typeof actual !== "number" || !Number.isFinite(actual)) {
    reportWa(i, c, actual, total);
    reportProgress(i + 1, total);
    continue;
  }
  const expected = c.expected;
  const diff = Math.abs(actual - expected);
  if (diff > 1e-5 && diff / Math.max(Math.abs(expected), 1e-9) > 1e-5) {
    reportWa(i, c, actual, total);
  }
  reportProgress(i + 1, total);
}
reportAc(total);
