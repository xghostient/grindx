        import java.util.*;

class Judge {
        static TreeNode listToTree(List<Object> arr) {
    if (arr == null || arr.isEmpty() || arr.get(0) == null) return null;
    TreeNode root = new TreeNode(Common.toInt(arr.get(0)));
    Queue<TreeNode> queue = new LinkedList<>();
    queue.add(root);
    int i = 1;
    while (i < arr.size() && !queue.isEmpty()) {
        TreeNode node = queue.poll();
        if (i < arr.size()) {
            Object leftVal = arr.get(i++);
            if (leftVal != null) {
                node.left = new TreeNode(Common.toInt(leftVal));
                queue.add(node.left);
            }
        }
        if (i < arr.size()) {
            Object rightVal = arr.get(i++);
            if (rightVal != null) {
                node.right = new TreeNode(Common.toInt(rightVal));
                queue.add(node.right);
            }
        }
    }
    return root;
}

static List<Object> treeToList(TreeNode root) {
    List<Object> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new LinkedList<>();
    queue.add(root);
    while (!queue.isEmpty()) {
        TreeNode node = queue.poll();
        if (node == null) {
            result.add(null);
        } else {
            result.add(node.val);
            queue.add(node.left);
            queue.add(node.right);
        }
    }
    while (!result.isEmpty() && result.get(result.size() - 1) == null) result.remove(result.size() - 1);
    return result;
}

static TreeNode findNode(TreeNode root, int target) {
    if (root == null) return null;
    if (root.val == target) return root;
    TreeNode left = findNode(root.left, target);
    if (left != null) return left;
    return findNode(root.right, target);
}

static List<Integer> inorderValues(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    if (root == null) return out;
    out.addAll(inorderValues(root.left));
    out.add(root.val);
    out.addAll(inorderValues(root.right));
    return out;
}

static boolean isBalancedTree(TreeNode root) {
    return height(root) >= 0;
}

static int height(TreeNode root) {
    if (root == null) return 0;
    int left = height(root.left);
    int right = height(root.right);
    if (left < 0 || right < 0 || Math.abs(left - right) > 1) return -1;
    return 1 + Math.max(left, right);
}

static String intListString(int[] arr) {
    return Arrays.toString(arr);
}

static String intMatrixString(int[][] arr) {
    return Arrays.deepToString(arr);
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("convert-sorted-array-to-binary-search-tree");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    int[] nums = Common.toIntArray((List<Object>) ((List<Object>) c.get("input")).get(0));
    TreeNode root = new Solution().sortedArrayToBST(nums.clone());
    List<Integer> actualInorder = inorderValues(root);
    List<Integer> expected = new ArrayList<>();
    for (int value : nums) expected.add(value);
    if (!actualInorder.equals(expected) || !isBalancedTree(root)) {
        Common.reportWA(i, c.get("input"), expected.toString(), treeToList(root).toString(), total, (String) c.getOrDefault("category", ""));
    }
            Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
