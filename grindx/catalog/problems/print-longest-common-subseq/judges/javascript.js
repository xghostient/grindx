        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.printLCS;
          if (typeof fn !== "function") {
            console.error("Missing function: printLCS");
            process.exit(2);
          }
          const tc = loadCases("print-longest-common-subseq");
          const cases = tc.cases;
          const total = cases.length;
        function isSubsequence(needle, haystack) {
  let idx = 0;
  for (const ch of haystack) {
    if (idx < needle.length && needle[idx] === ch) idx++;
  }
  return idx === needle.length;
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0], c.input[1]);
  if (typeof actual !== "string" || actual.length !== c.expected || !isSubsequence(actual, c.input[0]) || !isSubsequence(actual, c.input[1])) {
    reportWa(i, c, actual, total);
  }
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
