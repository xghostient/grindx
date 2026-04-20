import java.util.*;

class Judge {
    static ListNode buildCycleList(int[] arr, int pos) {
        if (arr.length == 0) return null;
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
        return head;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("length-of-cycle");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            int pos = Common.toInt(input.get(1));
            int actual = new Solution().cycleLength(buildCycleList(arr, pos));
            int expected = Common.toInt(c.get("expected"));
            if (actual != expected) {
                Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
