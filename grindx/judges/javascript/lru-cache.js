/**
 * Judge for LRU Cache — design class pattern.
 */

const path = require("path");
const { loadCases, reportAc, reportWa, loadSolution, truncate } = require("./_common");

/**
 * Reference LRU implementation for generating expected output on large cases.
 */
class ReferenceLRU {
  constructor(capacity) {
    this.capacity = capacity;
    this.map = new Map();
  }
  get(key) {
    if (!this.map.has(key)) return -1;
    const val = this.map.get(key);
    this.map.delete(key);
    this.map.set(key, val);
    return val;
  }
  put(key, value) {
    if (this.map.has(key)) this.map.delete(key);
    this.map.set(key, value);
    if (this.map.size > this.capacity) {
      this.map.delete(this.map.keys().next().value);
    }
  }
}

function generateLargeCases() {
  const cases = [];
  const capacity = 1000;
  const numOps = 100000;
  let seed = 42;
  const rand = () => {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    return seed;
  };

  const operations = [];
  const opInputs = [];
  const expected = [];
  const ref = new ReferenceLRU(capacity);

  for (let i = 0; i < numOps; i++) {
    if (rand() % 3 === 0) {
      // ~33% get operations
      const key = rand() % 2000;
      operations.push("get");
      opInputs.push([key]);
      expected.push(ref.get(key));
    } else {
      // ~67% put operations
      const key = rand() % 2000;
      const val = rand() % 100000;
      operations.push("put");
      opInputs.push([key, val]);
      expected.push(null);
      ref.put(key, val);
    }
  }

  cases.push({
    input: [capacity],
    operations,
    op_inputs: opInputs,
    expected,
    category: "tle",
  });
  return cases;
}

function run(solutionPath) {
  // Class declarations are block-scoped in VM contexts and don't become
  // sandbox properties, so we wrap the solution in an IIFE that returns
  // the class explicitly.
  const fs = require("fs");
  const vm = require("vm");
  const code = fs.readFileSync(path.resolve(solutionPath), "utf-8");
  const wrapped = `(function() {\n${code}\nreturn { LRUCache };\n})()`;
  const result = vm.runInNewContext(wrapped, { require });
  const LRUCache = result.LRUCache;
  if (typeof LRUCache !== "function") {
    process.stderr.write("Solution does not export a LRUCache class\n");
    process.exit(2);
  }

  const tc = loadCases("lru-cache");
  const basicCases = tc.cases;
  const largeCases = generateLargeCases();
  const allCases = basicCases.concat(largeCases);
  const total = allCases.length;

  for (let i = 0; i < allCases.length; i++) {
    const c = allCases[i];
    const capacity = c.input[0];
    const ops = c.operations;
    const opInputs = c.op_inputs;
    const expectedResults = c.expected;

    const cache = new LRUCache(capacity);

    for (let j = 0; j < ops.length; j++) {
      const op = ops[j];
      const args = opInputs[j];
      let result;

      if (op === "get") {
        result = cache.get(args[0]);
      } else if (op === "put") {
        cache.put(args[0], args[1]);
        result = null;
      }

      if (expectedResults[j] !== null && result !== expectedResults[j]) {
        // Build a minimal preview for the failing operation
        const failInfo = {
          input: c.input,
          expected: `op[${j}] ${op}(${args.join(", ")}) => ${expectedResults[j]}`,
        };
        const wa = {
          verdict: "WA",
          failed_case: i,
          input_preview: truncate(JSON.stringify(failInfo.input)),
          expected_preview: truncate(failInfo.expected),
          actual_preview: truncate(JSON.stringify(result)),
          passed: i,
          total,
          category: c.category || "",
        };
        console.log(JSON.stringify(wa));
        process.exit(1);
      }
    }
  }
  reportAc(total);
}

run(process.argv[2]);
