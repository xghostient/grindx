import java.util.*;

class Judge {
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

    static List<Integer> linkedListToList(ListNode head) {
        List<Integer> out = new ArrayList<>();
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) {
                out.add(Integer.MIN_VALUE);
                return out;
            }
            out.add(head.val);
            head = head.next;
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("middle-of-the-linked-list");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            List<Integer> actual = linkedListToList(new Solution().middleNode(listToLinkedList(arr)));
            int[] expectedRaw = Common.toIntArray((List<Object>) c.get("expected"));
            List<Integer> expected = new ArrayList<>();
            for (int value : expectedRaw) expected.add(value);
            if (!actual.equals(expected)) {
                Common.reportWA(i, input, expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
