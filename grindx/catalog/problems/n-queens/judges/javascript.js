const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("n-queens");
const cases = tc.cases;
const total = cases.length;

function normalizeStrMatrix(rows) {
  if (!Array.isArray(rows)) return [];
  return rows.slice().sort((a, b) => JSON.stringify(a) < JSON.stringify(b) ? -1 : JSON.stringify(a) > JSON.stringify(b) ? 1 : 0);
}

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = normalizeStrMatrix(sol.solveNQueens(...c.input) || []);
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
