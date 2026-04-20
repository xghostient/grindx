const fs = require("fs");
const vm = require("vm");
const { loadCases, reportAc, reportProgress, reportWa } = require("./_common");

const source = fs.readFileSync(process.argv[2], "utf-8");
const wrapped = `(function() {\n${source}\nreturn { KthLargest };\n})()`;
const result = vm.runInNewContext(wrapped, { require });
const Cls = result.KthLargest;
if (typeof Cls !== "function") {
  process.stderr.write("Solution does not define a KthLargest class\n");
  process.exit(2);
}
const tc = loadCases("kth-largest-element-in-a-stream");
const cases = tc.cases;
const total = cases.length;

for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const obj = new Cls(c.input[0], c.input[1].slice());
  for (let j = 0; j < c.operations.length; j++) {
    const op = c.operations[j];
    const args = c.op_inputs[j];
    const expected = c.expected[j];
    let actual = null;
        if (op === "add") {
          actual = obj.add(...args);
        }
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      reportWa(i, { input: [`op ${j}: ${op}(${args.join(",")})`], expected }, actual, total);
    }
  }
  reportProgress(i + 1, total);
}

reportAc(total);
