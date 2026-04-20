const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("sudoku-solver");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const board = c.input[0].map(r => r.slice());
  sol.solveSudoku(board);
  if (JSON.stringify(board) !== JSON.stringify(c.expected)) failCase(i, c, board, total);
  reportProgress(i + 1, total);
}
reportAc(total);
