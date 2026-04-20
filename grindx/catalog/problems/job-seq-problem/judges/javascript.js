const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("job-seq-problem");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.jobSequencing(c.input[0].map(r => r.slice())) || [0, 0];
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
