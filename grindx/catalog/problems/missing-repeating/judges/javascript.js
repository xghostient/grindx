"use strict";

const {
  compare, loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function buildLargeCase(n, missing, repeating) {
  const arr = Array.from({ length: n }, (_, i) => i + 1);
  arr[missing - 1] = repeating;
  return {
    input: [arr],
    expected: [repeating, missing],
    category: "stress",
  };
}

function generateLargeCases() {
  const n = 100000;
  return [
    buildLargeCase(n, 1, n),
    buildLargeCase(n, n, Math.floor(n / 2)),
    buildLargeCase(n, 42424, 99999),
  ];
}

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.findMissingRepeating;
  if (typeof fn !== "function") {
    console.error("Missing function: findMissingRepeating");
    process.exit(2);
  }

  const tc = loadCases("missing-repeating");
  const cases = tc.cases.concat(generateLargeCases());
  const total = cases.length;
  for (let i = 0; i < cases.length; i += 1) {
    const testCase = cases[i];
    const arg0 = [...testCase.input[0]];
    const result = fn(arg0);
    const actual = result;
    if (!compare(actual, testCase.expected, "exact")) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
