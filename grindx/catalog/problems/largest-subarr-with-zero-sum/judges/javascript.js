"use strict";

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.maxLen;
  if (typeof fn !== "function") {
    console.error("Missing function: maxLen");
    process.exit(2);
  }

  const tc = loadCases("largest-subarr-with-zero-sum");
  const total = tc.cases.length;
  for (let i = 0; i < tc.cases.length; i += 1) {
    const testCase = tc.cases[i];
    const arg0 = [...testCase.input[0]];
    const result = fn(arg0);
    const actual = Array.isArray(result) ? Array.from(result) : result;
    if (JSON.stringify(actual) !== JSON.stringify(testCase.expected)) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
