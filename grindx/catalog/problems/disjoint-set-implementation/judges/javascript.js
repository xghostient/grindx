const path = require("path");
const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const tc = loadCases("disjoint-set-implementation");
  const cases = tc.cases;
  const total = cases.length;

  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const dsu = new sol.DSU(c.input[0]);
    for (let j = 0; j < c.operations.length; j++) {
      const op = c.operations[j];
      const args = c.op_inputs[j];
      const expected = c.expected[j];
      const actual = op === "union" ? dsu.union(args[0], args[1]) : dsu.find(args[0]) === dsu.find(args[1]);
      if (actual !== expected) reportWa(i, { input: [`op ${j}: ${op}(${args.join(",")})`], expected }, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
