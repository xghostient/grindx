const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("word-search-ii");
const cases = tc.cases;
const total = cases.length;


for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const board = c.input[0].map((row) => row.slice());
  const words = c.input[1].slice();
  const result = sol.findWords(board, words);
  const actual = Array.isArray(result) ? result.slice().sort() : result;
  const expected = Array.isArray(c.expected) ? c.expected.slice().sort() : c.expected;
  if (JSON.stringify(actual) !== JSON.stringify(expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}
reportAc(total);
