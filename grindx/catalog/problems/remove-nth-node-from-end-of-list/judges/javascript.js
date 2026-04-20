/**
 * Judge for Remove Nth Node From End of List — function pattern, linked list I/O.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  listToLinkedList, linkedListToList, reportProgress
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  const arr = [];
  for (let k = 0; k < 30; k++) arr.push((k * 7) % 11);
  const removeExpected = (values, n) => values.filter((_, idx) => idx !== (values.length - n));
  cases.push({ input: [arr, 30], expected: removeExpected(arr, 30), category: "stress" });
  cases.push({ input: [arr, 15], expected: removeExpected(arr, 15), category: "stress" });
  cases.push({ input: [arr, 1], expected: removeExpected(arr, 1), category: "stress" });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const removeNthFromEnd = sol.removeNthFromEnd;
  if (typeof removeNthFromEnd !== "function") {
    process.stderr.write("Solution does not export a removeNthFromEnd function\n");
    process.exit(2);
  }

  const tc = loadCases("remove-nth-node-from-end-of-list");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const arr = c.input[0];
    const n = c.input[1];
    const head = listToLinkedList([...arr]);
    const resultHead = removeNthFromEnd(head, n);
    const result = linkedListToList(resultHead);
    const expected = c.expected;

    if (JSON.stringify(result) !== JSON.stringify(expected)) {
      reportWa(i, c, result, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
