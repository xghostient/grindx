/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */

const path = require("path");
const { loadCases, reportAc, reportWa, loadSolution } = require("./_common");

function generateLargeCases() {
  // Deterministic PRNG (simple LCG, same seed as Python random.seed(42))
  // We use a fixed set of large inputs for TLE detection.
  const cases = [];
  for (const n of [10000, 100000]) {
    const nums = [];
    let seed = 42;
    const rand = () => {
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      return (seed % 2000000001) - 1000000000;
    };
    for (let k = 0; k < n; k++) nums.push(rand());
    // Plant a known answer
    const i = Math.abs(rand()) % n;
    let j = Math.abs(rand()) % n;
    while (j === i) j = (j + 1) % n;
    const target = nums[i] + nums[j];
    cases.push({ input: [nums, target], expected_indices: [i, j], category: "tle" });
  }
  return cases;
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

    if (i < basicCases.length) {
      const expected = c.expected;
      if (JSON.stringify([...result].sort((a, b) => a - b)) !==
          JSON.stringify([...expected].sort((a, b) => a - b))) {
        reportWa(i, c, result, total);
      }
    } else {
      // Large cases — validate answer
      if (!Array.isArray(result) || result.length !== 2 ||
          result[0] === result[1] ||
          nums[result[0]] + nums[result[1]] !== target) {
        reportWa(i, c, result, total);
      }
    }
  }
  reportAc(total);
}

run(process.argv[2]);
