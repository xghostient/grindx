import java.util.*;

/**
 * Judge for Linked List Cycle — function pattern, boolean result.
 *
 * NOTE: The user's Solution.java defines a top-level ListNode class, which is
 * a different type from Common.ListNode. Therefore, linked-list serialization
 * helpers are inlined here using the user's ListNode directly.
 *
 * Input format: [values, pos] where pos is the index the tail connects to
 * (-1 means no cycle).
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
        while (head != null) {
            result.add(head.val);
            head = head.next;
        }
        return result;
    }

    /** Build a linked list with an optional cycle. pos = -1 means no cycle. */
    static ListNode buildCyclicList(int[] arr, int pos) {
        if (arr.length == 0) return null;
        ListNode head = new ListNode(arr[0]);
        ListNode curr = head;
        ListNode cycleTarget = (pos == 0) ? head : null;
        for (int i = 1; i < arr.length; i++) {
            curr.next = new ListNode(arr[i]);
            curr = curr.next;
            if (i == pos) cycleTarget = curr;
        }
        if (pos >= 0 && cycleTarget != null) {
            curr.next = cycleTarget;
        }
        return head;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("linked-list-cycle");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<Object[]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            int pos = Common.toInt(input.get(1));

            ListNode head = buildCyclicList(arr, pos);
            Solution sol = new Solution();
            boolean result = sol.hasCycle(head);

            boolean expected = (Boolean) c.get("expected");

            if (result != expected) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected),
                    String.valueOf(result), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            int[] arr = (int[]) largeCases.get(li)[0];
            int pos = (int) largeCases.get(li)[1];
            boolean expected = (boolean) largeCases.get(li)[2];

            ListNode head = buildCyclicList(arr, pos);
            Solution sol = new Solution();
            boolean result = sol.hasCycle(head);

            if (result != expected) {
                Common.reportWA(idx, "hidden input (" + arr.length + " nodes, pos=" + pos + ")",
                    String.valueOf(expected), String.valueOf(result), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    private static List<Object[]> generateLargeCases() {
        List<Object[]> cases = new ArrayList<>();
        int n = 10000;
        int[] arr = new int[n];
        for (int k = 0; k < n; k++) {
            arr[k] = ((k * 17) % 200001) - 100000;
        }
        cases.add(new Object[]{arr, 5000, true});
        cases.add(new Object[]{arr, -1, false});

        return cases;
    }
}
