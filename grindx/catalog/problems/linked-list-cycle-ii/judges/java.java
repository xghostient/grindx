import java.util.*;

class Judge {
    static class Built {
        ListNode head;
        List<ListNode> nodes;
        Built(ListNode head, List<ListNode> nodes) {
            this.head = head;
            this.nodes = nodes;
        }
    }

    static Built buildCycleList(int[] arr, int pos) {
        if (arr.length == 0) return new Built(null, new ArrayList<>());
        ListNode head = new ListNode(arr[0]);
        List<ListNode> nodes = new ArrayList<>();
        nodes.add(head);
        ListNode cur = head;
        for (int i = 1; i < arr.length; i++) {
            cur.next = new ListNode(arr[i]);
            cur = cur.next;
            nodes.add(cur);
        }
        if (pos >= 0) cur.next = nodes.get(pos);
        return new Built(head, nodes);
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("linked-list-cycle-ii");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            int pos = Common.toInt(input.get(1));
            Built built = buildCycleList(arr, pos);
            ListNode result = new Solution().detectCycle(built.head);
            int actual = -1;
            for (int idx = 0; idx < built.nodes.size(); idx++) {
                if (result == built.nodes.get(idx)) {
                    actual = idx;
                    break;
                }
            }
            int expected = Common.toInt(c.get("expected"));
            if (actual != expected) {
                Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
