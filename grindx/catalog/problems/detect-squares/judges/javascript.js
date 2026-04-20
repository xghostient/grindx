const fs = require("fs");
const vm = require("vm");
const { loadCases, reportAc, reportProgress, reportWa } = require("./_common");

const source = fs.readFileSync(process.argv[2], "utf-8");
const wrapped = `(function() {\n${source}\nreturn { DetectSquares };\n})()`;
const result = vm.runInNewContext(wrapped, { require });
const Cls = result.DetectSquares;
if (typeof Cls !== "function") {
  process.stderr.write("Solution does not define a DetectSquares class\n");
  process.exit(2);
}
const tc = loadCases("detect-squares");
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
        if (op === "add") {
          obj.add(...args); actual = null;
        }
        if (op === "count") {
          actual = obj.count(...args);
        }
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      reportWa(i, { input: [`op ${j}: ${op}(${args.join(",")})`], expected }, actual, total);
    }
  }
  reportProgress(i + 1, total);
}

reportAc(total);
