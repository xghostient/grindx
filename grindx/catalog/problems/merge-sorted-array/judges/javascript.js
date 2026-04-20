const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("merge-sorted-array");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const nums1 = c.input[0].slice();
  const nums2 = c.input[2].slice();
  sol.merge(nums1, c.input[1], nums2, c.input[3]);
  if (JSON.stringify(nums1) !== JSON.stringify(c.expected)) failCase(i, c, nums1, total);
  reportProgress(i + 1, total);
}
reportAc(total);
