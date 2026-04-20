        const path = require("path");
        const { adjListToGraph, graphToAdjList, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function cloneMatrix(matrix) {
  return matrix.map((row) => row.slice());
}

function stringRowsToGrid(rows) {
  return rows.map((row) => row.split(""));
}

function gridToStringRows(grid) {
  return grid.map((row) => row.join(""));
}

function normalizePairs(values) {
  return values.map((pair) => [pair[0], pair[1]]).sort((a, b) => (a[0] - b[0]) || (a[1] - b[1]));
}

function graphSharesIdentity(original, clone) {
  if (!original || !clone) return false;
  const originalNodes = new Set();
  const stack = [original];
  while (stack.length) {
    const node = stack.pop();
    if (originalNodes.has(node)) continue;
    originalNodes.add(node);
    for (const neighbor of node.neighbors || []) stack.push(neighbor);
  }
  const seen = new Set();
  const cloneStack = [clone];
  while (cloneStack.length) {
    const node = cloneStack.pop();
    if (seen.has(node)) continue;
    if (originalNodes.has(node)) return true;
    seen.add(node);
    for (const neighbor of node.neighbors || []) cloneStack.push(neighbor);
  }
  return false;
}


        function run(solutionPath) {
          const sol = loadSolution(path.resolve(solutionPath));
          const tc = loadCases("walls-and-gates");
          const cases = tc.cases;
          const total = cases.length;
        const fn = sol.wallsAndGates;
for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const rooms = cloneMatrix(c.input[0]);
  fn(rooms);
  if (JSON.stringify(rooms) !== JSON.stringify(c.expected)) reportWa(i, c, rooms, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
