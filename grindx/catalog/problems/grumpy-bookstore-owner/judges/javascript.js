"use strict";

const {
  compare, loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function expected(customers, grumpy, minutes) {
  let base = 0;
  for (let i = 0; i < customers.length; i += 1) {
    if (grumpy[i] === 0) base += customers[i];
  }
  let extra = 0;
  for (let i = 0; i < minutes; i += 1) {
    if (grumpy[i] === 1) extra += customers[i];
  }
  let best = extra;
  for (let i = minutes; i < customers.length; i += 1) {
    if (grumpy[i] === 1) extra += customers[i];
    if (grumpy[i - minutes] === 1) extra -= customers[i - minutes];
    if (extra > best) best = extra;
  }
  return base + best;
}

function generateLargeCases() {
  const n = 20000;
  const cases = [];
  for (let shift = 0; shift < 8; shift += 1) {
    const customers = [];
    const grumpy = [];
    for (let i = 0; i < n; i += 1) {
      customers.push((i + shift) % 2 === 0 ? 1000 : 1);
      grumpy.push(1);
    }
    const minutes = Math.floor(n / 2) + (shift % 5);
    cases.push({ input: [customers, grumpy, minutes], expected: expected(customers, grumpy, minutes), category: "tle" });
  }
  for (let shift = 0; shift < 8; shift += 1) {
    const customers = [];
    const grumpy = [];
    for (let i = 0; i < n; i += 1) {
      customers.push(((i + shift) % 9) * 111);
      grumpy.push((i + shift) % 3 === 0 ? 1 : 0);
    }
    const minutes = Math.floor(n / 2) + (shift % 7);
    cases.push({ input: [customers, grumpy, minutes], expected: expected(customers, grumpy, minutes), category: "tle" });
  }
  for (let shift = 0; shift < 8; shift += 1) {
    const customers = [];
    const grumpy = [];
    for (let i = 0; i < n; i += 1) {
      customers.push((i + shift) % 4 < 2 ? 5 : 20);
      grumpy.push((i + shift) % 5 ? 1 : 0);
    }
    const minutes = Math.floor(n / 3) + (shift % 11);
    cases.push({ input: [customers, grumpy, minutes], expected: expected(customers, grumpy, minutes), category: "tle" });
  }
  for (let shift = 0; shift < 8; shift += 1) {
    const customers = [];
    const grumpy = [];
    for (let i = 0; i < n; i += 1) {
      customers.push(997 - ((i + shift) % 11));
      grumpy.push((i + shift) % 2 === 0 ? 1 : 0);
    }
    const minutes = n - 123 - (shift % 17);
    cases.push({ input: [customers, grumpy, minutes], expected: expected(customers, grumpy, minutes), category: "tle" });
  }
  return cases;
}

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const fn = mod.maxSatisfied;
  if (typeof fn !== "function") {
    console.error("Missing function: maxSatisfied");
    process.exit(2);
  }

  const tc = loadCases("grumpy-bookstore-owner");
  const cases = tc.cases.concat(generateLargeCases());
  const total = cases.length;
  for (let i = 0; i < cases.length; i += 1) {
    const testCase = cases[i];
    const arg0 = [...testCase.input[0]];
    const arg1 = [...testCase.input[1]];
    const arg2 = testCase.input[2];
    const result = fn(arg0, arg1, arg2);
    const actual = result;
    if (!compare(actual, testCase.expected, "exact")) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
