        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.unboundedKnapsack;
          if (typeof fn !== "function") {
            console.error("Missing function: unboundedKnapsack");
            process.exit(2);
          }
          const tc = loadCases("subseq-09-knapsack");
          const cases = tc.cases;
          const total = cases.length;
        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0], c.input[1], c.input[2].slice(), c.input[3].slice());
  if (actual !== c.expected) reportWa(i, c, actual, total);
          reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
