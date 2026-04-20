const path = require("path");
const { loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

class Node {
  constructor(val = 0, next = null, random = null) {
    this.val = val;
    this.next = next;
    this.random = random;
  }
}

function buildRandom(spec) {
  if (!spec.length) return { head: null, nodes: [] };
  const nodes = spec.map((item) => new Node(item[0]));
  for (let i = 0; i < nodes.length - 1; i++) nodes[i].next = nodes[i + 1];
  for (let i = 0; i < nodes.length; i++) {
    const target = spec[i][1];
    nodes[i].random = target === null ? null : nodes[target];
  }
  return { head: nodes[0], nodes };
}

function randomRepr(head) {
  const nodes = [];
  const index = new Map();
  let cur = head;
  let steps = 0;
  while (cur && steps < 100000) {
    index.set(cur, nodes.length);
    nodes.push(cur);
    cur = cur.next;
    steps++;
  }
  if (cur) return [[-2147483648, null]];
  return nodes.map((node) => [node.val, node.random === null ? null : index.get(node.random)]);
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.copyRandomList;
  const tc = loadCases("copy-list-with-random-pointer");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    let spec = c.input[0];
    if (JSON.stringify(spec) === JSON.stringify([[]])) spec = [];
    const built = buildRandom(spec);
    const result = fn(built.head);
    const actual = randomRepr(result);
    let deepOk = true;
    let cur = result;
    while (cur) {
      if (built.nodes.includes(cur)) {
        deepOk = false;
        break;
      }
      cur = cur.next;
    }
    if (JSON.stringify(actual) !== JSON.stringify(c.expected) || !deepOk) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
