        const path = require("path");
        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function cloneStringMatrix(matrix) { return matrix.map((row) => row.slice()); }
function normalizePaths(paths) {
  return (paths || []).map((path) => path.slice()).sort((a, b) => a.join("\u0001").localeCompare(b.join("\u0001")));
}
function validateAlienOrder(words, order) {
  const chars = new Set(words.join("").split(""));
  if (typeof order !== "string" || order.length !== chars.size) return false;
  const seen = new Set(order.split(""));
  if (seen.size !== chars.size) return false;
  for (const ch of chars) if (!seen.has(ch)) return false;
  const rank = new Map();
  for (let i = 0; i < order.length; i++) rank.set(order[i], i);
  for (let i = 0; i + 1 < words.length; i++) {
    const a = words[i], b = words[i + 1];
    let j = 0;
    while (j < a.length && j < b.length && a[j] === b[j]) j++;
    if (j === Math.min(a.length, b.length)) {
      if (a.length > b.length) return false;
      continue;
    }
    if (rank.get(a[j]) > rank.get(b[j])) return false;
  }
  return true;
}


        function run(solutionPath) {
          const sol = loadSolution(path.resolve(solutionPath));
          const tc = loadCases("alien-dictionary");
          const cases = tc.cases;
          const total = cases.length;
        const fn = sol.alienOrder;
for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0].slice());
  if (c.expected === "") {
    if (actual !== "") reportWa(i, c, actual, total);
  } else if (!validateAlienOrder(c.input[0], actual)) {
    reportWa(i, c, actual, total);
  }
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
