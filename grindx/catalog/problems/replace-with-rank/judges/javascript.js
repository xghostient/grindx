const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("replace-with-rank");
const cases = tc.cases;
const total = cases.length;



for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.replaceWithRank(c.input[0].slice());
  const actualNorm = Array.isArray(actual) ? actual.slice() : actual;
  if (JSON.stringify(actualNorm) !== JSON.stringify(c.expected)) reportWa(i, c, actualNorm, total);
  reportProgress(i + 1, total);
}
reportAc(total);
