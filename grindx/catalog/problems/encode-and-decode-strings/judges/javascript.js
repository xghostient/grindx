        const path = require("path");
        const {
          loadCases, loadSolution, reportAc, reportProgress, reportWa
        } = require("./_common");

        function normalizeStringGroups(groups) {
  return groups
    .map(group => [...group].sort())
    .sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
}

function deriveProbeStrings(strs) {
  return strs.map(value => value + "#probe").concat(["|probe|"]);
}

function toArrayOrValue(value) {
  if (value === null || value === undefined || typeof value === "string") return value;
  try {
    return Array.from(value);
  } catch (_) {
    return value;
  }
}


        const sol = loadSolution(process.argv[2]);
        const tc = loadCases("encode-and-decode-strings");
        const cases = tc.cases;
        const total = cases.length;

        for (let i = 0; i < cases.length; i++) {
  const testCase = cases[i];
  const strs = [...testCase.input[0]];
  const encoded = sol.encode([...strs]);
  const actual = sol.decode(encoded);
  sol.encode(deriveProbeStrings([...strs]));
  const roundtrip = sol.decode(encoded);
  if (JSON.stringify(actual) !== JSON.stringify(testCase.expected) || JSON.stringify(roundtrip) !== JSON.stringify(testCase.expected)) {
    reportWa(i, testCase, actual, total);
  }
  reportProgress(i + 1, total);
}

        reportAc(total);
