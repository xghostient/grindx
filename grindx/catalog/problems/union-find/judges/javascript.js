"use strict";

const {
  loadCases, reportAc, reportWa, loadSolution, reportProgress
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  for (let variant = 0; variant < 4; variant += 1) {
    const n = 100000;
    const unions = [];
    for (let i = 0; i < n - 1; i += 1) unions.push([i, i + 1]);
    let queries = [];
    if (variant === 0) {
      for (let i = 0; i < 100000; i += 1) queries.push([0, n - 1]);
    } else if (variant === 1) {
      for (let i = 0; i < 100000; i += 1) queries.push([0, n - 1 - i]);
    } else if (variant === 2) {
      for (let i = 0; i < 100000; i += 1) queries.push([i, n - 1]);
    } else {
      for (let i = 0; i < 50000; i += 1) {
        queries.push([0, Math.floor(n / 2)]);
        queries.push([Math.floor(n / 3), n - 1]);
      }
    }
    cases.push({ input: [n, unions, queries], expected: Array(queries.length).fill(true), category: "tle" });
  }
  return cases;
}

function run(solutionPath) {
  const mod = loadSolution(solutionPath);
  const UnionFind = mod.UnionFind;
  if (typeof UnionFind !== "function") {
    console.error("Missing class: UnionFind");
    process.exit(2);
  }

  const tc = loadCases("union-find");
  const cases = tc.cases.concat(generateLargeCases());
  const total = cases.length;
  for (let i = 0; i < cases.length; i += 1) {
    const testCase = cases[i];
    const [n, unions, queries] = testCase.input;
    const uf = new UnionFind(n);
    for (const [x, y] of unions) {
      uf.union(x, y);
    }
    const actual = queries.map(([x, y]) => Boolean(uf.connected(x, y)));
    if (JSON.stringify(actual) !== JSON.stringify(testCase.expected)) {
      reportWa(i, testCase, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
