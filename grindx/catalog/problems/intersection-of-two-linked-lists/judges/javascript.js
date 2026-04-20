const path = require("path");
const { ListNode, linkedListToList, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function buildList(values) {
  if (!values.length) return null;
  const head = new ListNode(values[0]);
  let cur = head;
  for (let i = 1; i < values.length; i++) {
    cur.next = new ListNode(values[i]);
    cur = cur.next;
  }
  return head;
}

function tail(head) {
  let cur = head;
  while (cur && cur.next) cur = cur.next;
  return cur;
}

function buildIntersection(a, b, shared) {
  const sharedHead = buildList(shared);
  let headA = buildList(a);
  let headB = buildList(b);
  if (headA === null) headA = sharedHead;
  else if (sharedHead !== null) tail(headA).next = sharedHead;
  if (headB === null) headB = sharedHead;
  else if (sharedHead !== null) tail(headB).next = sharedHead;
  return { headA, headB, sharedHead };
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.getIntersectionNode;
  const tc = loadCases("intersection-of-two-linked-lists");
  const cases = tc.cases;
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const built = buildIntersection(c.input[0], c.input[1], c.input[2]);
    const result = fn(built.headA, built.headB);
    if (result !== built.sharedHead) {
      reportWa(i, c, linkedListToList(result), total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
