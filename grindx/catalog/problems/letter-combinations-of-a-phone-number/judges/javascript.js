const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("letter-combinations-of-a-phone-number");
const cases = tc.cases;
const total = cases.length;

function normalizeStrList(items) {
  if (!Array.isArray(items)) return [];
  return items.slice().sort();
}

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = normalizeStrList(sol.letterCombinations(...c.input) || []);
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) failCase(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
