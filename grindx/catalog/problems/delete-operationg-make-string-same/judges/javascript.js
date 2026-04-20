        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.minDistance;
          if (typeof fn !== "function") {
            console.error("Missing function: minDistance");
            process.exit(2);
          }
          const tc = loadCases("delete-operationg-make-string-same");
          const cases = tc.cases;
          const total = cases.length;
        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0], c.input[1]);
  if (actual !== c.expected) reportWa(i, c, actual, total);
          reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
