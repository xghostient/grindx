import java.util.*;

/**
 * Judge for Merge K Sorted Lists — function pattern, linked list array I/O.
 *
 * NOTE: The user's Solution.java defines a top-level ListNode class, which is
 * a different type from Common.ListNode. Therefore, linked-list serialization
 * helpers are inlined here using the user's ListNode directly.
 *
 * Input format: [array_of_arrays] where each sub-array is a sorted linked list.
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
        Map<String, Object> tc = Common.loadCases("merge-k-sorted-lists");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<int[][]> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            List<Object> listsRaw = (List<Object>) input.get(0);

            ListNode[] lists = new ListNode[listsRaw.size()];
            for (int j = 0; j < listsRaw.size(); j++) {
                int[] arr = Common.toIntArray((List<Object>) listsRaw.get(j));
                lists[j] = listToLinkedList(arr);
            }

            Solution sol = new Solution();
            ListNode resultHead = sol.mergeKLists(lists);
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
            int[][] rawLists = largeCases.get(li);

            ListNode[] lists = new ListNode[rawLists.length];
            for (int j = 0; j < rawLists.length; j++) {
                lists[j] = listToLinkedList(rawLists[j]);
            }

            Solution sol = new Solution();
            ListNode resultHead = sol.mergeKLists(lists);
            List<Integer> result = linkedListToList(resultHead);

            // Compute expected: flatten all arrays, sort
            List<Integer> expected = new ArrayList<>();
            for (int[] arr : rawLists) {
                for (int v : arr) expected.add(v);
            }
            Collections.sort(expected);

            if (!result.equals(expected)) {
                Common.reportWA(idx, "hidden input (" + rawLists.length + " lists)",
                    "merged sorted list", result.toString(), total, "stress");
            }
        }

        Common.reportAC(total);
    }

    private static List<int[][]> generateLargeCases() {
        List<int[][]> cases = new ArrayList<>();
        int[][] dense = new int[100][];
        for (int i = 0; i < dense.length; i++) {
            int[] arr = new int[100];
            for (int j = 0; j < arr.length; j++) {
                arr[j] = (((i * 97) + (j * 29)) % 20001) - 10000;
            }
            Arrays.sort(arr);
            dense[i] = arr;
        }
        cases.add(dense);

        int[][] singleton = new int[10000][];
        for (int i = 0; i < singleton.length; i++) {
            singleton[i] = new int[]{((i * 37) % 20001) - 10000};
        }
        cases.add(singleton);

        int[][] sparse = new int[10000][];
        for (int i = 0; i < sparse.length; i++) sparse[i] = new int[0];
        sparse[123] = new int[]{-5, -5, 0, 3};
        sparse[5000] = new int[]{-1, 2, 2};
        sparse[9999] = new int[]{4};
        cases.add(sparse);
        return cases;
    }
}
