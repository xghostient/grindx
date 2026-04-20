import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    private static ListNode buildListNode(List<Object> values) {
        if (values.isEmpty()) {
            return null;
        }
        ListNode head = new ListNode(Common.toInt(values.get(0)));
        ListNode curr = head;
        for (int i = 1; i < values.size(); i++) {
            curr.next = new ListNode(Common.toInt(values.get(i)));
            curr = curr.next;
        }
        return head;
    }
@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("spiral-matrix-iv");
    List<Object> cases = (List<Object>) tc.get("cases");
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int arg0 = Common.toInt(input.get(0));
            int arg1 = Common.toInt(input.get(1));
            ListNode arg2 = buildListNode((List<Object>) input.get(2));
            int[][] expected = Common.toIntMatrix((List<Object>) c.get("expected"));

                    Solution sol = new Solution();
                    int[][] result = sol.spiralMatrix(arg0, arg1, arg2);
                    var actual = result;
            if (!Arrays.deepEquals(actual, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.deepToString(expected), Arrays.deepToString(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
