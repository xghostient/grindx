const fs = require("fs");
const vm = require("vm");
const { loadCases, reportAc, reportProgress, reportWa } = require("./_common");

const source = fs.readFileSync(process.argv[2], "utf-8");
const wrapped = `(function() {\n${source}\nreturn { TimeMap };\n})()`;
const result = vm.runInNewContext(wrapped, { require });
const Cls = result.TimeMap;
if (typeof Cls !== "function") {
  process.stderr.write("Solution does not define a TimeMap class\n");
  process.exit(2);
}
const tc = loadCases("time-based-key-value-store");
const cases = tc.cases;
const total = cases.length;

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const obj = new Cls();
  for (let j = 0; j < c.operations.length; j++) {
    const op = c.operations[j];
    const args = c.op_inputs[j];
    const expected = c.expected[j];
    let actual = null;
    if (op === "TimeMap") {
      actual = null;
    } else if (op === "set") {
      obj.set(args[0], args[1], args[2]);
      actual = null;
    } else if (op === "get") {
      actual = obj.get(args[0], args[1]);
    }
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      reportWa(i, { input: [`op ${j}: ${op}(${args.join(",")})`], expected }, actual, total);
    }
  }
  reportProgress(i + 1, total);
}

reportAc(total);
