/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */

const path = require("path");
const { loadCases, reportAc, reportProgress, reportWa, loadSolution } = require("./_common");

function generateLargeCases() {
  const cases = [];
  const n = 10000;

  {
    const nums = [-500000000];
    for (let i = 1; i < n - 1; i++) {
      nums.push(200000000 + ((i * 7919) % 700000000));
    }
    nums.push(123456789);
    cases.push({
      input: [nums, -376543211],
      expected_indices: [0, n - 1],
      category: "tle",
    });
  }

  {
    const nums = [];
    for (let i = 0; i < n; i++) {
      nums.push(300000000 + ((i * 1237) % 600000000));
    }
    const dupI = 137;
    const dupJ = 9862;
    nums[dupI] = 123456789;
    nums[dupJ] = 123456789;
    cases.push({
      input: [nums, 246913578],
      expected_indices: [dupI, dupJ],
      category: "tle",
    });
  }

  {
    const nums = [];
    for (let i = 0; i < n; i++) {
      nums.push(1 + ((i * 48271) % 999999998));
    }
    const lowI = 4000;
    const highI = 7000;
    nums[lowI] = -1000000000;
    nums[highI] = 1000000000;
    cases.push({
      input: [nums, 0],
      expected_indices: [lowI, highI],
      category: "tle",
    });
  }

  {
    const nums = [];
    for (let i = 0; i < n; i++) {
      nums.push(1 + ((i * 8191) % 999999999));
    }
    const zeroI = 2500;
    const zeroJ = 7500;
    nums[zeroI] = 0;
    nums[zeroJ] = 0;
    cases.push({
      input: [nums, 0],
      expected_indices: [zeroI, zeroJ],
      category: "tle",
    });
  }

  return cases;
}

function isValidIndexPair(result, size) {
  return Array.isArray(result) &&
    result.length === 2 &&
    result.every((idx) => Number.isInteger(idx) && idx >= 0 && idx < size);
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const twoSum = sol.twoSum;
  if (typeof twoSum !== "function") {
    process.stderr.write("Solution does not export a twoSum function\n");
    process.exit(2);
  }

  const tc = loadCases("two-sum");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const [nums, target] = c.input;
    const result = twoSum([...nums], target); // copy to prevent mutation

    if (!isValidIndexPair(result, nums.length)) {
      reportWa(i, c, result, total);
    }

    if (i < basicCases.length) {
      const expected = c.expected;
      if (JSON.stringify([...result].sort((a, b) => a - b)) !==
          JSON.stringify([...expected].sort((a, b) => a - b))) {
        reportWa(i, c, result, total);
      }
    } else {
      const expected = c.expected_indices;
      if (JSON.stringify([...result].sort((a, b) => a - b)) !==
          JSON.stringify([...expected].sort((a, b) => a - b))) {
        reportWa(i, c, result, total);
      }
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
