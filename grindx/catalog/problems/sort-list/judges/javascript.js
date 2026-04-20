const path = require("path");
const { listToLinkedList, linkedListToList, loadCases, loadSolution, reportAc, reportProgress, reportWa } = require("./_common");

function generateLargeCases() {
  const descending = Array.from({ length: 50000 }, (_, i) => 50000 - i);
  const mixed = Array.from({ length: 50000 }, (_, i) => ((i * 8191) % 200001) - 100000);
  const duplicates = Array.from({ length: 50000 }, (_, i) => ((i * 37) % 31) - 15);
  return [
    {
      input: [descending],
      expected: Array.from({ length: 50000 }, (_, i) => i + 1),
      category: "stress",
    },
    {
      input: [mixed],
      expected: [...mixed].sort((a, b) => a - b),
      category: "stress",
    },
    {
      input: [duplicates],
      expected: [...duplicates].sort((a, b) => a - b),
      category: "stress",
    },
  ];
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const fn = sol.sortList;
  const tc = loadCases("sort-list");
  const cases = tc.cases.concat(generateLargeCases());
  const total = cases.length;
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const head = listToLinkedList([...c.input[0]]);
    const actual = linkedListToList(fn(head));
    if (JSON.stringify(actual) !== JSON.stringify(c.expected)) {
      reportWa(i, c, actual, total);
    }
    reportProgress(i + 1, total);
  }
  reportAc(total);
}

run(process.argv[2]);
