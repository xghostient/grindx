        const path = require("path");
        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function cloneMatrix(matrix) {
  return matrix.map((row) => row.slice());
}

function normalizeAccounts(accounts) {
  if (!Array.isArray(accounts)) return null;
  const out = [];
  for (const account of accounts) {
    if (!Array.isArray(account) || account.length === 0) return null;
    const name = account[0];
    const emails = Array.from(new Set(account.slice(1))).sort();
    out.push([name, ...emails]);
  }
  out.sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
  return out;
}


        function run(solutionPath) {
          const sol = loadSolution(path.resolve(solutionPath));
          const tc = loadCases("minimum-height-trees");
          const cases = tc.cases;
          const total = cases.length;
        const fn = sol.findMinHeightTrees;
for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = (fn(c.input[0], cloneMatrix(c.input[1])) || []).slice().sort((a, b) => a - b);
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
