const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("top-k-frequent-elements");
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

function sortedIntList(values) {
  if (!Array.isArray(values)) return [];
  return values.slice().map(Number).sort((a, b) => a - b);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sortedIntList(sol.topKFrequent(c.input[0].slice(), c.input[1]));
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
