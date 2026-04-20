        const path = require("path");
const fs = require("fs");
const vm = require("vm");
const { listToTree, treeToList, loadCases, reportAc, reportProgress, reportWa } = require("./_common");

            function loadCodec(solutionPath) {
              const code = fs.readFileSync(path.resolve(solutionPath), "utf-8");
              const wrapped = `(function(){
${code}
return { Codec };
})()`;
              return vm.runInNewContext(wrapped, { require }).Codec;
            }
function findNode(root, target) {
  if (root == null) return null;
  if (root.val === target) return root;
  return findNode(root.left, target) || findNode(root.right, target);
}

function inorderValues(root) {
  if (root == null) return [];
  return inorderValues(root.left).concat([root.val], inorderValues(root.right));
}

function preorderValues(root) {
  if (root == null) return [];
  return [root.val].concat(preorderValues(root.left), preorderValues(root.right));
}

function postorderValues(root) {
  if (root == null) return [];
  return postorderValues(root.left).concat(postorderValues(root.right), [root.val]);
}

function levelOrderValues(root) {
  if (root == null) return [];
  const out = [];
  const queue = [[root, 0]];
  while (queue.length) {
        const [node, depth] = queue.shift();
        if (depth === out.length) out.push([]);
        out[depth].push(node.val);
        if (node.left) queue.push([node.left, depth + 1]);
        if (node.right) queue.push([node.right, depth + 1]);
      }
      return out;
    }

function isBalancedTree(root) {
  function height(node) {
    if (node == null) return 0;
    const left = height(node.left);
    const right = height(node.right);
    if (left === null || right === null || Math.abs(left - right) > 1) return null;
        return 1 + Math.max(left, right);
      }
      return height(root) !== null;
    }


        function run(solutionPath) {
          const tc = loadCases("serialize-and-deserialize-binary-tree");
          const cases = tc.cases;
          const total = cases.length;
        const Codec = loadCodec(solutionPath);
const codec = new Codec();
for (let i = 0; i < cases.length; i++) {
  const c = cases[i];
  const root = listToTree(c.input[0]);
  const actual = treeToList(codec.deserialize(codec.serialize(root)));
  if (JSON.stringify(actual) !== JSON.stringify(c.expected)) reportWa(i, c, actual, total);
  reportProgress(i + 1, total);
}

          reportAc(total);
        }

        run(process.argv[2]);
