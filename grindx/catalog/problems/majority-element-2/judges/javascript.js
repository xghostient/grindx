"use strict";

const {
  compare, loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function generateLargeCases() {
  const stressOne = Array.from({ length: 16666 }, (_, i) => i + 3)
    .concat(Array(16667).fill(1), Array(16667).fill(2));
  const stressTwo = Array.from({ length: 33333 }, (_, i) => i + 2)
    .concat(Array(16667).fill(1));
  const stressThree = Array.from({ length: 16666 }, (_, i) => -(i + 3))
    .concat(Array(16667).fill(-1), Array(16667).fill(-2));
  const stressFour = Array.from({ length: 33333 }, (_, i) => 1000000000 - i)
    .concat(Array(16667).fill(999999999));
  const stressFive = Array.from({ length: 16666 }, (_, i) => 500000000 + i)
    .concat(Array(16667).fill(7), Array(16667).fill(8));
  const stressSix = Array.from({ length: 33333 }, (_, i) => -(500000000 + i))
    .concat(Array(16667).fill(-7));
  const stressSeven = Array.from({ length: 16666 }, (_, i) => 250000000 + i)
    .concat(Array(16667).fill(123456789), Array(16667).fill(987654321));
  const stressEight = Array.from({ length: 33333 }, (_, i) => -(250000000 + i))
    .concat(Array(16667).fill(-123456789));
  const cases = [
    { input: [stressOne], expected: [1, 2], category: "stress" },
    { input: [stressTwo], expected: [1], category: "stress" },
    { input: [stressThree], expected: [-2, -1], category: "stress" },
    { input: [stressFour], expected: [999999999], category: "stress" },
    { input: [stressFive], expected: [7, 8], category: "stress" },
    { input: [stressSix], expected: [-7], category: "stress" },
    { input: [stressSeven], expected: [123456789, 987654321], category: "stress" },
    { input: [stressEight], expected: [-123456789], category: "stress" },
  ];
  return Array.from({ length: 4 }, () => cases).flat();
}

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.majorityElement;
  if (typeof fn !== "function") {
    console.error("Missing function: majorityElement");
    process.exit(2);
  }

  const tc = loadCases("majority-element-2");
  const cases = tc.cases.concat(generateLargeCases());
  const total = cases.length;
  for (let i = 0; i < cases.length; i += 1) {
    const testCase = cases[i];
    const arg0 = [...testCase.input[0]];
    const result = fn(arg0);
    const actual = result;
    if (!compare(actual, testCase.expected, "unordered")) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
