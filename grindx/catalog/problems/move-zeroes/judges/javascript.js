const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("move-zeroes");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const nums = c.input[0].slice();
  sol.moveZeroes(nums);
  if (JSON.stringify(nums) !== JSON.stringify(c.expected)) failCase(i, c, nums, total);
  reportProgress(i + 1, total);
}
reportAc(total);
