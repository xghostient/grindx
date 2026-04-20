const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("peak-element-02");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const mat = c.input[0].map(row => row.slice());
  const result = sol.findPeakGrid(mat.map(row => row.slice()));
  const rows = mat.length, cols = mat[0].length;
  let valid = Array.isArray(result) && result.length === 2;
  let r = 0, cc = 0;
  if (valid) {
    [r, cc] = result;
    valid = Number.isInteger(r) && Number.isInteger(cc) && r >= 0 && r < rows && cc >= 0 && cc < cols;
  }
  if (valid) {
    const val = mat[r][cc];
    if (r > 0 && mat[r - 1][cc] >= val) valid = false;
    if (r < rows - 1 && mat[r + 1][cc] >= val) valid = false;
    if (cc > 0 && mat[r][cc - 1] >= val) valid = false;
    if (cc < cols - 1 && mat[r][cc + 1] >= val) valid = false;
  }
  if (!valid) failCase(i, c, result, total);
  reportProgress(i + 1, total);
}
reportAc(total);
