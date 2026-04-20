const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("peak-element");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const nums = c.input[0].slice();
  const idx = sol.findPeakElement(nums.slice());
  const n = nums.length;
  let valid = idx >= 0 && idx < n;
  if (valid && idx > 0 && nums[idx] <= nums[idx - 1]) valid = false;
  if (valid && idx < n - 1 && nums[idx] <= nums[idx + 1]) valid = false;
  if (!valid) failCase(i, c, idx, total);
  reportProgress(i + 1, total);
}
reportAc(total);
