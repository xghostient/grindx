"use strict";

const {
  compare, loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.setZeroes;
  if (typeof fn !== "function") {
    console.error("Missing function: setZeroes");
    process.exit(2);
  }

  const tc = loadCases("set-matrix-zeroes");
  const total = tc.cases.length;
  for (let i = 0; i < tc.cases.length; i += 1) {
    const testCase = tc.cases[i];
    const arg0 = testCase.input[0].map((row) => [...row]);
    const result = fn(arg0);
    const actual = arg0;
    if (!compare(actual, testCase.expected, "exact")) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
