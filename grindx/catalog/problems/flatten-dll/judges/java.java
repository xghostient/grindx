import java.util.*;

class Judge {
    static Node buildBottom(List<Object> rows) {
        List<Node> heads = new ArrayList<>();
        for (Object rowObj : rows) {
            List<Object> row = (List<Object>) rowObj;
            if (row.isEmpty()) continue;
            Node head = new Node(Common.toInt(row.get(0)));
            Node cur = head;
            for (int i = 1; i < row.size(); i++) {
                cur.bottom = new Node(Common.toInt(row.get(i)));
                cur = cur.bottom;
            }
            heads.add(head);
        }
        for (int i = 0; i + 1 < heads.size(); i++) heads.get(i).next = heads.get(i + 1);
        return heads.isEmpty() ? null : heads.get(0);
    }

    static List<Integer> bottomRepr(Node head) {
        List<Integer> out = new ArrayList<>();
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        while (head != null) {
            if (!seen.add(head)) return Collections.singletonList(Integer.MIN_VALUE);
            out.add(head.val);
            head = head.bottom;
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("flatten-dll");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> rows = (List<Object>) ((List<Object>) c.get("input")).get(0);
            List<Integer> actual = bottomRepr(new Solution().flatten(buildBottom(rows)));
            int[] expectedRaw = Common.toIntArray((List<Object>) c.get("expected"));
            List<Integer> expected = new ArrayList<>();
            for (int value : expectedRaw) expected.add(value);
            if (!actual.equals(expected)) {
                Common.reportWA(i, c.get("input"), expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
