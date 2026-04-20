        const path = require("path");
        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function cloneMatrix(matrix) { return matrix.map((row) => row.slice()); }
function cloneWeightedAdj(adj) { return adj.map((row) => row.map((edge) => edge.slice())); }


        function run(solutionPath) {
          const sol = loadSolution(path.resolve(solutionPath));
          const tc = loadCases("shortest-path-ug");
          const cases = tc.cases;
          const total = cases.length;
        const fn = sol.shortestPath;
for (let i = 0; i < cases.length; i++) { const c = cases[i]; const actual = fn(c.input[0], cloneMatrix(c.input[1]), c.input[2]); if (JSON.stringify(actual) !== JSON.stringify(c.expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
