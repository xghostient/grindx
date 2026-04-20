const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("4sum");
const cases = tc.cases;
const total = cases.length;

function normalizeIntMatrix(rows) {
  if (!Array.isArray(rows)) return [];
  return rows
    .map((row) => Array.isArray(row) ? row.slice().map(Number).sort((a, b) => a - b) : [])
    .sort((a, b) => {
      if (a.length !== b.length) return a.length - b.length;
      for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) return a[i] - b[i];
      }
      return 0;
    });
}

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = normalizeIntMatrix(sol.fourSum(c.input[0].slice(), c.input[1]) || []);
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
