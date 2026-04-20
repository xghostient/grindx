        const path = require("path");
        const {
          loadCases, loadSolution, reportAc, reportProgress, reportWa
        } = require("./_common");



        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("valid-anagram");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const testCase = cases[i];
  const actual = sol.isAnagram(testCase.input[0], testCase.input[1]);
  if (actual !== testCase.expected) reportWa(i, testCase, actual, total);
  reportProgress(i + 1, total);
}

        reportAc(total);
