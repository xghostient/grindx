const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("first-bad-version");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const n = c.input[0][0], bad = c.input[0][1];
  global.isBadVersion = (v) => v >= bad;
  const actual = sol.firstBadVersion(n);
  if (actual !== c.expected) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
