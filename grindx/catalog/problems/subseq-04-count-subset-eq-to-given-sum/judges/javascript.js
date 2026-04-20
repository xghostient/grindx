        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.countSubsets;
          if (typeof fn !== "function") {
            console.error("Missing function: countSubsets");
            process.exit(2);
          }
          const tc = loadCases("subseq-04-count-subset-eq-to-given-sum");
          const cases = tc.cases;
          const total = cases.length;
        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0].slice(), c.input[1]);
  if (actual !== c.expected) reportWa(i, c, actual, total);
          reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
