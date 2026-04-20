import java.util.*;

/**
 * Judge for Reorder List — in-place linked list modification.
 *
 * NOTE: The user's Solution.java defines a top-level ListNode class, which is
 * a different type from Common.ListNode. Therefore, linked-list serialization
 * helpers are inlined here using the user's ListNode directly.
 *
 * The function modifies the list in-place (void return). We serialize the
 * modified list and compare against expected output.
 */
class Judge {

    /** Build a linked list from an int array using the user's top-level ListNode. */
    static ListNode listToLinkedList(int[] arr) {
        if (arr.length == 0) return null;
        ListNode head = new ListNode(arr[0]);
        ListNode curr = head;
        for (int i = 1; i < arr.length; i++) {
            curr.next = new ListNode(arr[i]);
            curr = curr.next;
        }
        return head;
    }

    /** Convert a linked list back to a List<Integer> for comparison. */
    static List<Integer> linkedListToList(ListNode head) {
        List<Integer> result = new ArrayList<>();
        Set<ListNode> seen = new HashSet<>();
        int steps = 0;
        while (head != null && steps < 100000) {
            if (!seen.add(head)) {
                result.add(Integer.MIN_VALUE);
                return result;
            }
            result.add(head.val);
            head = head.next;
            steps++;
        }
        if (head != null) {
            result.add(Integer.MIN_VALUE);
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("reorder-list");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<int[]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));

            ListNode head = listToLinkedList(arr);
            Solution sol = new Solution();
            sol.reorderList(head);
            List<Integer> result = linkedListToList(head);

            int[] expectedArr = Common.toIntArray((List<Object>) c.get("expected"));
            List<Integer> expected = new ArrayList<>();
            for (int v : expectedArr) expected.add(v);

            if (!result.equals(expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, expected.toString(),
                    result.toString(), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            int[] arr = largeCases.get(li);

            ListNode head = listToLinkedList(arr);
            Solution sol = new Solution();
            sol.reorderList(head);
            List<Integer> result = linkedListToList(head);

            // Compute expected reorder: L0 -> Ln -> L1 -> Ln-1 -> ...
            List<Integer> expected = computeReorder(arr);

            if (!result.equals(expected)) {
                Common.reportWA(idx, "hidden input (" + arr.length + " elements)",
                    "reordered list", result.toString(), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    /** Compute the expected reorder pattern for an array. */
    private static List<Integer> computeReorder(int[] arr) {
        List<Integer> expected = new ArrayList<>();
        int left = 0, right = arr.length - 1;
        boolean pickLeft = true;
        while (left <= right) {
            if (pickLeft) {
                expected.add(arr[left]);
                left++;
            } else {
                expected.add(arr[right]);
                right--;
            }
            pickLeft = !pickLeft;
        }
        return expected;
    }

    private static List<int[]> generateLargeCases() {
        List<int[]> cases = new ArrayList<>();
        int[] even = new int[50000];
        for (int k = 0; k < even.length; k++) {
            even[k] = (k % 1000) + 1;
        }
        cases.add(even);

        int[] odd = new int[49999];
        for (int k = 0; k < odd.length; k++) {
            odd[k] = ((k * 7) % 1000) + 1;
        }
        cases.add(odd);
        return cases;
    }
}
