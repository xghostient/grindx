/**
 * Judge for Reorder List — in-place linked list mutation.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  listToLinkedList, linkedListToList, reportProgress
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  const makeExpected = (arr) => {
    const expected = [];
    let lo = 0;
    let hi = arr.length - 1;
    while (lo <= hi) {
      expected.push(arr[lo]);
      if (lo !== hi) expected.push(arr[hi]);
      lo++;
      hi--;
    }
    return expected;
  };

  const even = [];
  for (let k = 0; k < 50000; k++) even.push((k % 1000) + 1);
  const odd = [];
  for (let k = 0; k < 49999; k++) odd.push(((k * 7) % 1000) + 1);

  cases.push({ input: [even], expected: makeExpected(even), category: "stress" });
  cases.push({ input: [odd], expected: makeExpected(odd), category: "stress" });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const reorderList = sol.reorderList;
  if (typeof reorderList !== "function") {
    process.stderr.write("Solution does not export a reorderList function\n");
    process.exit(2);
  }

  const tc = loadCases("reorder-list");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const head = listToLinkedList([...c.input[0]]);
    reorderList(head);
    const result = linkedListToList(head);
    const expected = c.expected;

    if (JSON.stringify(result) !== JSON.stringify(expected)) {
      reportWa(i, c, result, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
