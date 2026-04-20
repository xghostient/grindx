import java.util.*;

class Judge {
    static class Built {
        DLLNode head;
        List<DLLNode> nodes;
        Built(DLLNode head, List<DLLNode> nodes) {
            this.head = head;
            this.nodes = nodes;
        }
    }

    static Built listToDLL(int[] arr) {
        if (arr.length == 0) return new Built(null, new ArrayList<>());
        DLLNode head = new DLLNode(arr[0]);
        List<DLLNode> nodes = new ArrayList<>();
        nodes.add(head);
        DLLNode cur = head;
        for (int i = 1; i < arr.length; i++) {
            DLLNode node = new DLLNode(arr[i]);
            node.prev = cur;
            cur.next = node;
            cur = node;
            nodes.add(node);
        }
        return new Built(head, nodes);
    }

    static List<Integer> dllToList(DLLNode head) {
        List<Integer> out = new ArrayList<>();
        Set<DLLNode> seen = new HashSet<>();
        DLLNode prev = null;
        while (head != null) {
            if (!seen.add(head) || head.prev != prev) {
                return Collections.singletonList(Integer.MIN_VALUE);
            }
            out.add(head.val);
            prev = head;
            head = head.next;
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("remove-duplicates-dll");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            Built built = listToDLL(Common.toIntArray((List<Object>) input.get(0)));
            DLLNode head = built.head;
            List<DLLNode> nodes = built.nodes;
            List<Integer> actual = dllToList(new Solution().removeDuplicates(head));
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
