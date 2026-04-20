const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("armstrong-number");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  let actual = sol.isArmstrong(c.input[0]);
  if (actual === undefined || actual === null) actual = false;
  if (actual !== c.expected) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
