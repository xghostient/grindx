const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("find-first-and-last-position-of-element-in-sorted-array");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.searchRange(c.input[0].slice(), c.input[1]);
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
