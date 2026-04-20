import java.util.*;

/**
 * Judge for Remove Nth Node From End of List — function pattern, linked list I/O.
 *
 * NOTE: The user's Solution.java defines a top-level ListNode class, which is
 * a different type from Common.ListNode. Therefore, linked-list serialization
 * helpers are inlined here using the user's ListNode directly.
 *
 * Input format: [values, n] where n is the position from the end to remove.
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
        Map<String, Object> tc = Common.loadCases("remove-nth-node-from-end-of-list");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<int[][]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            int n = Common.toInt(input.get(1));

            ListNode head = listToLinkedList(arr);
            Solution sol = new Solution();
            ListNode resultHead = sol.removeNthFromEnd(head, n);
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
            int[] arr = largeCases.get(li)[0];
            int n = largeCases.get(li)[1][0];

            ListNode head = listToLinkedList(arr);
            Solution sol = new Solution();
            ListNode resultHead = sol.removeNthFromEnd(head, n);
            List<Integer> result = linkedListToList(resultHead);

            // Compute expected: remove element at index (arr.length - n)
            List<Integer> expected = new ArrayList<>();
            int removeIdx = arr.length - n;
            for (int k = 0; k < arr.length; k++) {
                if (k != removeIdx) expected.add(arr[k]);
            }

            if (!result.equals(expected)) {
                Common.reportWA(idx, "hidden input (" + arr.length + " elements, n=" + n + ")",
                    "list with node removed", result.toString(), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    private static List<int[][]> generateLargeCases() {
        List<int[][]> cases = new ArrayList<>();
        int size = 30;
        int[] arr = new int[size];
        for (int k = 0; k < size; k++) {
            arr[k] = (k * 7) % 11;
        }
        cases.add(new int[][]{arr, {30}});
        cases.add(new int[][]{arr, {15}});
        cases.add(new int[][]{arr, {1}});
        return cases;
    }
}
