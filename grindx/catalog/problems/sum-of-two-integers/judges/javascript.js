"use strict";

const {
  compare, loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.getSum;
  if (typeof fn !== "function") {
    console.error("Missing function: getSum");
    process.exit(2);
  }

  const tc = loadCases("sum-of-two-integers");
  const total = tc.cases.length;
  for (let i = 0; i < tc.cases.length; i += 1) {
    const testCase = tc.cases[i];
    const arg0 = testCase.input[0];
    const arg1 = testCase.input[1];
    const result = fn(arg0, arg1);
    const actual = result;
    if (!compare(actual, testCase.expected, "exact")) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
