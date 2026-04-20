/**
 * Judge for Merge Two Sorted Lists — function pattern, linked list I/O.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  listToLinkedList, linkedListToList, reportProgress
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  const list2Only = [];
  for (let k = 0; k < 50; k++) list2Only.push((((k * 7) + 3) % 201) - 100);
  list2Only.sort((a, b) => a - b);

  const arr1 = [];
  const arr2 = [];
  for (let k = 0; k < 25; k++) arr1.push((((k * 9) + 1) % 201) - 100);
  for (let k = 0; k < 25; k++) arr2.push((((k * 11) + 5) % 201) - 100);
  arr1.sort((a, b) => a - b);
  arr2.sort((a, b) => a - b);

  cases.push({ input: [[], list2Only], expected: list2Only, category: "stress" });
  cases.push({
    input: [arr1, arr2],
    expected: [...arr1, ...arr2].sort((a, b) => a - b),
    category: "stress",
  });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const mergeTwoLists = sol.mergeTwoLists;
  if (typeof mergeTwoLists !== "function") {
    process.stderr.write("Solution does not export a mergeTwoLists function\n");
    process.exit(2);
  }

  const tc = loadCases("merge-two-sorted-lists");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const head1 = listToLinkedList([...c.input[0]]);
    const head2 = listToLinkedList([...c.input[1]]);
    const resultHead = mergeTwoLists(head1, head2);
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
