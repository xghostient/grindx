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

    static ListNode tail(ListNode head) {
        ListNode cur = head;
        while (cur != null && cur.next != null) cur = cur.next;
        return cur;
    }

    static class Built {
        ListNode headA;
        ListNode headB;
        ListNode shared;
        Built(ListNode headA, ListNode headB, ListNode shared) {
            this.headA = headA;
            this.headB = headB;
            this.shared = shared;
        }
    }

    static Built buildIntersection(int[] a, int[] b, int[] sharedValues) {
        ListNode shared = listToLinkedList(sharedValues);
        ListNode headA = listToLinkedList(a);
        ListNode headB = listToLinkedList(b);
        if (headA == null) headA = shared;
        else if (shared != null) tail(headA).next = shared;
        if (headB == null) headB = shared;
        else if (shared != null) tail(headB).next = shared;
        return new Built(headA, headB, shared);
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
        Map<String, Object> tc = Common.loadCases("intersection-of-two-linked-lists");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            Built built = buildIntersection(
                Common.toIntArray((List<Object>) input.get(0)),
                Common.toIntArray((List<Object>) input.get(1)),
                Common.toIntArray((List<Object>) input.get(2))
            );
            ListNode actualNode = new Solution().getIntersectionNode(built.headA, built.headB);
            if (actualNode != built.shared) {
                Common.reportWA(i, input, c.get("expected"), linkedListToList(actualNode).toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
