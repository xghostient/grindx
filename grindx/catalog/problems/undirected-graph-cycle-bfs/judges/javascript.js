        const path = require("path");
        const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

        function cloneMatrix(matrix) {
  return matrix.map((row) => row.slice());
}

function validTopologicalOrder(order, v, adj) {
  if (!Array.isArray(order) || order.length !== v) return false;
  const pos = new Map();
  for (let i = 0; i < order.length; i++) {
    const node = order[i];
    if (!Number.isInteger(node) || node < 0 || node >= v || pos.has(node)) return false;
    pos.set(node, i);
  }
  for (let node = 0; node < v; node++) {
    if (!pos.has(node)) return false;
    for (const nei of adj[node]) {
      if (pos.get(node) >= pos.get(nei)) return false;
    }
  }
  return true;
}

function validCourseOrder(order, numCourses, prerequisites) {
  if (!Array.isArray(order) || order.length !== numCourses) return false;
  const pos = new Map();
  for (let i = 0; i < order.length; i++) {
    const course = order[i];
    if (!Number.isInteger(course) || course < 0 || course >= numCourses || pos.has(course)) return false;
    pos.set(course, i);
  }
  for (const [course, prereq] of prerequisites) {
    if (pos.get(prereq) >= pos.get(course)) return false;
  }
  return true;
}


        function run(solutionPath) {
          const sol = loadSolution(path.resolve(solutionPath));
          const tc = loadCases("undirected-graph-cycle-bfs");
          const cases = tc.cases;
          const total = cases.length;
        const fn = sol.isCycle;
for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const actual = fn(c.input[0], cloneMatrix(c.input[1]));
  if (actual !== c.expected) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
