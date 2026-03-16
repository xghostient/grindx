/**
 * Judge for Rotate Array — in-place mutation pattern.
 */

const path = require("path");
const { loadCases, reportAc, reportWa, loadSolution } = require("./_common");

function generateLargeCases() {
  const cases = [];
  const n = 100000;
  let seed = 42;
  const rand = () => {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    return (seed % 2000000001) - 1000000000;
  };

  // Large case 1: large k < n
  const nums1 = [];
  for (let i = 0; i < n; i++) nums1.push(rand());
  const k1 = Math.abs(rand()) % n;
  const ek1 = k1 % n;
  const expected1 = nums1.slice(n - ek1).concat(nums1.slice(0, n - ek1));
  cases.push({ input: [nums1, k1], expected: expected1, category: "tle" });

  // Large case 2: k > n
  const nums2 = [];
  for (let i = 0; i < n; i++) nums2.push(rand());
  const k2 = n + Math.abs(rand()) % n;
  const ek2 = k2 % n;
  const expected2 = nums2.slice(n - ek2).concat(nums2.slice(0, n - ek2));
  cases.push({ input: [nums2, k2], expected: expected2, category: "tle" });

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
  }
  reportAc(total);
}

run(process.argv[2]);
