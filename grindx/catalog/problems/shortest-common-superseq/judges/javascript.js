        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.shortestCommonSupersequence;
          if (typeof fn !== "function") {
            console.error("Missing function: shortestCommonSupersequence");
            process.exit(2);
          }
          const tc = loadCases("shortest-common-superseq");
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
  if (typeof actual !== "string") reportWa(i, c, actual, total);
  if (actual.length !== c.expected || !isSubsequence(c.input[0], actual) || !isSubsequence(c.input[1], actual)) {
    reportWa(i, c, actual, total);
  }
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
