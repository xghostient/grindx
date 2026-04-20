        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function isValidMinWindow(source, target, expected, actual) {
  if (typeof actual !== "string") return false;
  if (actual.length !== expected.length) return false;
  if (expected === "") return actual === "";
  if (!source.includes(actual)) return false;
  const need = new Map();
  const have = new Map();
  for (const ch of target) need.set(ch, (need.get(ch) || 0) + 1);
  for (const ch of actual) have.set(ch, (have.get(ch) || 0) + 1);
  for (const [ch, count] of need.entries()) {
    if ((have.get(ch) || 0) < count) return false;
  }
  return true;
}


        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("substring-containing-all-three-chars");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = sol.numberOfSubstrings(c.input[0]);
  if (actual !== c.expected) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

        reportAc(total);
