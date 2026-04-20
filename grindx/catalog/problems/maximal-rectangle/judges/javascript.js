        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("maximal-rectangle");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const matrix = c.input[0].map((row) => row.split(""));
  const actual = sol.maximalRectangle(matrix);
  if (actual !== c.expected) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

        reportAc(total);
