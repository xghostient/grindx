import java.util.*;

/**
 * Judge for Reverse Linked List — function pattern, linked list I/O.
 *
 * NOTE: The user's Solution.java defines a top-level ListNode class, which is
 * a different type from Common.ListNode. Therefore, linked-list serialization
 * helpers are inlined here using the user's ListNode directly.
 */
class Judge {

    /** Build a linked list from an int array using the user's top-level ListNode. */
    static ListNode listToLinkedList(int[] arr) {
        if (arr.length == 0) return null;
        ListNode head = new ListNode(arr[0]);
        ListNode cur = head;
        for (int i = 1; i < arr.length; i++) {
            cur.next = new ListNode(arr[i]);
            cur = cur.next;
        }
        return head;
    }

    /** Convert a linked list back to a List<Integer> for comparison. */
    static List<Integer> linkedListToList(ListNode head) {
        List<Integer> result = new ArrayList<>();
        Set<ListNode> seen = new HashSet<>();
        ListNode cur = head;
        int steps = 0;
        while (cur != null && steps < 100000) {
            if (!seen.add(cur)) {
                result.add(Integer.MIN_VALUE);
                return result;
            }
            result.add(cur.val);
            cur = cur.next;
            steps++;
        }
        if (cur != null) {
            result.add(Integer.MIN_VALUE);
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("reverse-linked-list");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large case for TLE detection
        List<int[]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));

            ListNode head = listToLinkedList(arr);
            Solution sol = new Solution();
            ListNode resultHead = sol.reverseList(head);
            List<Integer> result = linkedListToList(resultHead);

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
            ListNode resultHead = sol.reverseList(head);
            List<Integer> result = linkedListToList(resultHead);

            // Expected: reversed input
            List<Integer> expected = new ArrayList<>();
            for (int k = arr.length - 1; k >= 0; k--) expected.add(arr[k]);

            if (!result.equals(expected)) {
                Common.reportWA(idx, "max input (" + arr.length + " elements)",
                    "reversed list", result.toString(), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    private static List<int[]> generateLargeCases() {
        List<int[]> cases = new ArrayList<>();
        int n = 5000;
        int[] arr = new int[n];
        for (int k = 0; k < n; k++) {
            arr[k] = ((k * 73) % 1001) - 500;
        }
        cases.add(arr);
        return cases;
    }
}
