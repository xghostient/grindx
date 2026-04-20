        "use strict";

        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function run(solutionPath) {
          const sol = loadSolution(solutionPath);
          const fn = sol.printLIS;
          if (typeof fn !== "function") {
            console.error("Missing function: printLIS");
            process.exit(2);
          }
          const tc = loadCases("lis-02-print-lis");
          const cases = tc.cases;
          const total = cases.length;
        function isSubsequenceList(seq, arr) {
  let idx = 0;
  for (const value of arr) {
    if (idx < seq.length && seq[idx] === value) idx++;
  }
  return idx === seq.length;
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const arr = c.input[0].slice();
  const actual = fn(arr);
  let valid = Array.isArray(actual) && actual.length === c.expected;
  if (valid) {
    for (let j = 0; j + 1 < actual.length; j++) {
      if (actual[j] >= actual[j + 1]) valid = false;
    }
    if (valid && !isSubsequenceList(actual, arr)) valid = false;
  }
  if (!valid) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
