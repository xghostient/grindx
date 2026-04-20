/**
 * Judge for Maximum Depth of Binary Tree — function pattern, tree input, int return.
 */

const path = require("path");
const { loadCases, reportAc, reportProgress, reportWa, loadSolution, listToTree } = require("./_common");

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const maxDepth = sol.maxDepth;
  if (typeof maxDepth !== "function") {
    process.stderr.write("Solution does not export a maxDepth function\n");
    process.exit(2);
  }

  const tc = loadCases("maximum-depth-of-binary-tree");
  const allCases = tc.cases;
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const arr = c.input[0];
    const root = listToTree(arr);
    const result = maxDepth(root);
    const expected = c.expected;

    if (result !== expected) {
      reportWa(i, c, result, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
