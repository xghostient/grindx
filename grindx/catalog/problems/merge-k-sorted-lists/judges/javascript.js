/**
 * Judge for Merge K Sorted Lists — function pattern, linked list I/O.
 */

const path = require("path");
const {
  loadCases, reportAc, reportWa, loadSolution,
  listToLinkedList, linkedListToList, reportProgress
} = require("./_common");

function generateLargeCases() {
  const cases = [];
  const denseLists = [];
  const allValues = [];
  for (let i = 0; i < 100; i++) {
    const arr = [];
    for (let j = 0; j < 100; j++) {
      const v = (((i * 97) + (j * 29)) % 20001) - 10000;
      arr.push(v);
      allValues.push(v);
    }
    arr.sort((a, b) => a - b);
    denseLists.push(arr);
  }
  cases.push({
    input: [denseLists],
    expected: allValues.sort((a, b) => a - b),
    category: "stress",
  });

  const singletonLists = [];
  const singletonExpected = [];
  for (let i = 0; i < 10000; i++) {
    const value = ((i * 37) % 20001) - 10000;
    singletonLists.push([value]);
    singletonExpected.push(value);
  }
  singletonExpected.sort((a, b) => a - b);
  cases.push({
    input: [singletonLists],
    expected: singletonExpected,
    category: "stress",
  });

  const sparseLists = Array.from({ length: 10000 }, () => []);
  sparseLists[123] = [-5, -5, 0, 3];
  sparseLists[5000] = [-1, 2, 2];
  sparseLists[9999] = [4];
  cases.push({
    input: [sparseLists],
    expected: [-5, -5, -1, 0, 2, 2, 3, 4],
    category: "stress",
  });
  return cases;
}

function run(solutionPath) {
  const sol = loadSolution(path.resolve(solutionPath));
  const mergeKLists = sol.mergeKLists;
  if (typeof mergeKLists !== "function") {
    process.stderr.write("Solution does not export a mergeKLists function\n");
    process.exit(2);
  }

  const tc = loadCases("merge-k-sorted-lists");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const arrays = c.input[0];
    const heads = arrays.map((arr) => listToLinkedList([...arr]));
    const resultHead = mergeKLists(heads);
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
