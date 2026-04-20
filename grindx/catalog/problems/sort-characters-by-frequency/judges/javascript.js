        const {
          loadCases, loadSolution, reportAc, reportProgress, reportWa
        } = require("./_common");

        function isValidLongestPalindrome(source, expected, actual) {
  return typeof actual === "string" &&
    actual === actual.split("").reverse().join("") &&
    source.includes(actual) &&
    actual.length === expected.length;
}

function isValidFrequencySort(source, actual) {
  if (typeof actual !== "string") return false;
  if (actual.length !== source.length) return false;
  const counts = new Map();
  for (const ch of source) counts.set(ch, (counts.get(ch) || 0) + 1);
  const seen = new Map();
  for (const ch of actual) seen.set(ch, (seen.get(ch) || 0) + 1);
  if (counts.size !== seen.size) return false;
  for (const [ch, count] of counts.entries()) {
    if (seen.get(ch) !== count) return false;
  }
  for (let i = 1; i < actual.length; i++) {
    if ((counts.get(actual[i - 1]) || 0) < (counts.get(actual[i]) || 0)) return false;
  }
  return true;
}


        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("sort-characters-by-frequency");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const testCase = cases[i];
  const actual = sol.frequencySort(testCase.input[0]);
  if (!isValidFrequencySort(testCase.input[0], actual)) reportWa(i, testCase, actual, total);
  reportProgress(i + 1, total);
}

        reportAc(total);
