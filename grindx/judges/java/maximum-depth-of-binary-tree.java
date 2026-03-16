import java.util.*;

/**
 * Judge for Maximum Depth of Binary Tree — function pattern, tree input, int return.
 *
 * NOTE: The user's Solution.java defines a top-level TreeNode class, which is
 * a different type from Common.TreeNode. Therefore, tree deserialization is
 * inlined here using the user's TreeNode directly.
 */
class Judge {

    /** Build a binary tree from a level-order list (with nulls) using the user's top-level TreeNode. */
    static TreeNode listToTree(List<Object> arr) {
        if (arr == null || arr.isEmpty() || arr.get(0) == null) return null;
        TreeNode root = new TreeNode(((Number) arr.get(0)).intValue());
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        int i = 1;
        while (i < arr.size() && !queue.isEmpty()) {
            TreeNode node = queue.poll();
            // Left child
            if (i < arr.size()) {
                Object leftVal = arr.get(i);
                i++;
                if (leftVal != null) {
                    node.left = new TreeNode(((Number) leftVal).intValue());
                    queue.add(node.left);
                }
            }
            // Right child
            if (i < arr.size()) {
                Object rightVal = arr.get(i);
                i++;
                if (rightVal != null) {
                    node.right = new TreeNode(((Number) rightVal).intValue());
                    queue.add(node.right);
                }
            }
        }
        return root;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("maximum-depth-of-binary-tree");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large case for TLE detection: complete binary tree of depth 14
        List<Object[]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            List<Object> treeArr = (List<Object>) input.get(0);

            TreeNode root = listToTree(treeArr);
            Solution sol = new Solution();
            int result = sol.maxDepth(root);

            int expected = Common.toInt(c.get("expected"));

            if (result != expected) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected),
                    String.valueOf(result), total, category);
            }
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            Object[] lc = largeCases.get(li);
            List<Object> treeArr = (List<Object>) lc[0];
            int expectedDepth = (int) lc[1];

            TreeNode root = listToTree(treeArr);
            Solution sol = new Solution();
            int result = sol.maxDepth(root);

            if (result != expectedDepth) {
                Common.reportWA(idx, "large input (" + treeArr.size() + " nodes)",
                    String.valueOf(expectedDepth), String.valueOf(result), total, "tle");
            }
        }

        Common.reportAC(total);
    }

    @SuppressWarnings("unchecked")
    private static List<Object[]> generateLargeCases() {
        List<Object[]> cases = new ArrayList<>();
        Random rng = new Random(42);
        int depth = 14;
        int n = (1 << depth) - 1; // 16383 nodes
        List<Object> arr = new ArrayList<>();
        for (int k = 0; k < n; k++) {
            arr.add(rng.nextInt(200001) - 100000);
        }
        cases.add(new Object[]{arr, depth});
        return cases;
    }
}
