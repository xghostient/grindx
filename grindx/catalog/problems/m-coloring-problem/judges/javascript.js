const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("m-coloring-problem");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const args = c.input.map(a => Array.isArray(a) ? (Array.isArray(a[0]) ? a.map(r => r.slice()) : a.slice()) : a);
  const actual = sol.graphColoring(...args) || false;
  if (actual !== c.expected) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
