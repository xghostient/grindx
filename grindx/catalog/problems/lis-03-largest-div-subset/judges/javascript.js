        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.largestDivisibleSubset;
          if (typeof fn !== "function") {
            console.error("Missing function: largestDivisibleSubset");
            process.exit(2);
          }
          const tc = loadCases("lis-03-largest-div-subset");
          const cases = tc.cases;
          const total = cases.length;
        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const arr = c.input[0].slice();
  const actual = fn(arr);
  let valid = Array.isArray(actual) && actual.length === c.expected && new Set(actual).size === actual.length && actual.every((v) => arr.includes(v));
  if (valid) {
    for (let x = 0; x < actual.length; x++) {
      for (let y = x + 1; y < actual.length; y++) {
        if (actual[x] % actual[y] !== 0 && actual[y] % actual[x] !== 0) valid = false;
      }
    }
  }
  if (!valid) reportWa(i, c, actual, total);
          reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
