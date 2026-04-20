        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("daily-temperatures");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.dailyTemperatures(c.input[0].slice());
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

        reportAc(total);
