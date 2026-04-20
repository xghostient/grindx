/**
 * Judge for Rotate Array — in-place mutation pattern.
 */

const path = require("path");
const { loadCases, reportAc, reportProgress, reportWa, loadSolution } = require("./_common");

function generateLargeCases() {
  const cases = [];
  for (const [n, k, start, step] of [
    [100000, 99999, -1000000000, 37],
    [100000, 87500, -999900000, 53],
    [100000, 75000, -999800000, 61],
    [100000, 62500, -999700000, 73],
    [100000, 50000, -999600000, 79],
    [100000, 37500, -999500000, 83],
    [100000, 25000, -999400000, 89],
    [99999, 99998, -999300000, 97],
  ]) {
    const nums = [];
    for (let i = 0; i < n; i++) nums.push(start + (i * step));
    const ek = k % n;
    const expected = ek === 0
      ? [...nums]
      : nums.slice(n - ek).concat(nums.slice(0, n - ek));
    cases.push({ input: [nums, k], expected, category: "tle" });
  }

  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const rotate = sol.rotate;
  if (typeof rotate !== "function") {
    process.stderr.write("Solution does not export a rotate function\n");
    process.exit(2);
  }

  const tc = loadCases("rotate-array");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const [nums, k] = c.input;
    const numsCopy = [...nums];
    rotate(numsCopy, k);
    const expected = c.expected;

    if (JSON.stringify(numsCopy) !== JSON.stringify(expected)) {
      reportWa(i, c, numsCopy, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
