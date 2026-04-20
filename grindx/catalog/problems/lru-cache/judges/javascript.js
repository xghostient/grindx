/**
 * Judge for LRU Cache — design class pattern.
 */

const path = require("path");
const { loadCases, reportAc, reportProgress, reportWa, loadSolution, truncate } = require("./_common");

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

function runLargeCase(LRUCache, total, caseIndex) {
  const capacity = 3000;
  const totalOps = 200000;
  const cache = new LRUCache(capacity);
  const ref = new ReferenceLRU(capacity);

  for (let key = 0; key < capacity; key++) {
    const value = (key * 97) % 100001;
    cache.put(key, value);
    ref.put(key, value);
  }

  for (let step = 0; step < totalOps - capacity; step++) {
    const key = (step * 1879) % capacity;
    if (step % 2 === 0) {
      const expected = ref.get(key);
      const result = cache.get(key);
      if (result !== expected) {
        reportWa(caseIndex, {
          input: [`stress op ${step}: get(${key})`],
          expected,
          category: "stress",
        }, result, total);
      }
    } else {
      const value = ((step * 7919) + key) % 100001;
      cache.put(key, value);
      ref.put(key, value);
    }
  }
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
  const total = basicCases.length + 1;

  for (let i = 0; i < basicCases.length; i++) {
    const c = basicCases[i];
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
    reportProgress(i + 1, total);
  }
  runLargeCase(LRUCache, total, basicCases.length);
  reportAc(total);
}

run(process.argv[2]);
