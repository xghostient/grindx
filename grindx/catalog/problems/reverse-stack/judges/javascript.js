const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");
const sol = loadSolution(process.argv[2]);
const tc = loadCases("reverse-stack");
const cases = tc.cases;
const total = cases.length;

function failCase(index, c, actual, total) {
  reportWa(index, c, actual, total);
}

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const stack = c.input[0].slice();
  sol.reverseStack(stack);
  if (JSON.stringify(stack) !== JSON.stringify(c.expected)) failCase(i, c, stack, total);
  reportProgress(i + 1, total);
}
reportAc(total);
