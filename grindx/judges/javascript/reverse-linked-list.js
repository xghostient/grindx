/**
 * Judge for Reverse Linked List — function pattern, linked list I/O.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  listToLinkedList, linkedListToList,
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  const n = 5000;
  let seed = 42;
  const rand = () => {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    return (seed % 2000001) - 1000000;
  };
  const arr = [];
  for (let k = 0; k < n; k++) arr.push(rand());
  const expected = [...arr].reverse();
  cases.push({ input: [arr], expected, category: "tle" });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const reverseList = sol.reverseList;
  if (typeof reverseList !== "function") {
    process.stderr.write("Solution does not export a reverseList function\n");
    process.exit(2);
  }

  const tc = loadCases("reverse-linked-list");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const arr = c.input[0];
    const head = listToLinkedList([...arr]);
    const resultHead = reverseList(head);
    const result = linkedListToList(resultHead);
    const expected = c.expected;

    if (JSON.stringify(result) !== JSON.stringify(expected)) {
      reportWa(i, c, result, total);
    }
  }
  reportAc(total);
}

run(process.argv[2]);
