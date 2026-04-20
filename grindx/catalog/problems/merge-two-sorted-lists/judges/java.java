import java.util.*;

/**
 * Judge for Merge Two Sorted Lists — function pattern, linked list I/O.
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
        Map<String, Object> tc = Common.loadCases("merge-two-sorted-lists");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<int[][]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr1 = Common.toIntArray((List<Object>) input.get(0));
            int[] arr2 = Common.toIntArray((List<Object>) input.get(1));

            ListNode list1 = listToLinkedList(arr1);
            ListNode list2 = listToLinkedList(arr2);
            Solution sol = new Solution();
            ListNode resultHead = sol.mergeTwoLists(list1, list2);
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
            int[] arr1 = largeCases.get(li)[0];
            int[] arr2 = largeCases.get(li)[1];

            ListNode list1 = listToLinkedList(arr1);
            ListNode list2 = listToLinkedList(arr2);
            Solution sol = new Solution();
            ListNode resultHead = sol.mergeTwoLists(list1, list2);
            List<Integer> result = linkedListToList(resultHead);

            // Expected: merge two sorted arrays
            int[] merged = new int[arr1.length + arr2.length];
            System.arraycopy(arr1, 0, merged, 0, arr1.length);
            System.arraycopy(arr2, 0, merged, arr1.length, arr2.length);
            Arrays.sort(merged);
            List<Integer> expected = new ArrayList<>();
            for (int v : merged) expected.add(v);

            if (!result.equals(expected)) {
                Common.reportWA(idx, "hidden input (" + arr1.length + " + " + arr2.length + " elements)",
                    "merged sorted list", result.toString(), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    private static List<int[][]> generateLargeCases() {
        List<int[][]> cases = new ArrayList<>();
        int[] list2Only = new int[50];
        for (int k = 0; k < list2Only.length; k++) {
            list2Only[k] = (((k * 7) + 3) % 201) - 100;
        }
        Arrays.sort(list2Only);
        cases.add(new int[][]{new int[0], list2Only});

        int[] arr1 = new int[25];
        int[] arr2 = new int[25];
        for (int k = 0; k < arr1.length; k++) {
            arr1[k] = (((k * 9) + 1) % 201) - 100;
            arr2[k] = (((k * 11) + 5) % 201) - 100;
        }
        Arrays.sort(arr1);
        Arrays.sort(arr2);
        cases.add(new int[][]{arr1, arr2});
        return cases;
    }
}
