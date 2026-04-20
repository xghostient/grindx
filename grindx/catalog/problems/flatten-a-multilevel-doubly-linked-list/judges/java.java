import java.util.*;

class Judge {
    static class MultiSpec {
        int val;
        List<MultiSpec> child;
    }

    static Node buildLevel(List<MultiSpec> spec) {
        if (spec == null || spec.isEmpty()) return null;
        Node head = null;
        Node prev = null;
        for (MultiSpec item : spec) {
            Node node = new Node(item.val);
            if (head == null) head = node;
            if (prev != null) {
                prev.next = node;
                node.prev = prev;
            }
            if (item.child != null && !item.child.isEmpty()) node.child = buildLevel(item.child);
            prev = node;
        }
        return head;
    }

    static List<Integer> flattenRepr(Node head) {
        List<Integer> out = new ArrayList<>();
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        Node prev = null;
        while (head != null) {
            if (!seen.add(head) || head.prev != prev || head.child != null) return Collections.singletonList(Integer.MIN_VALUE);
            out.add(head.val);
            prev = head;
            head = head.next;
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("flatten-a-multilevel-doubly-linked-list");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            String raw = c.get("input").toString();
            List<MultiSpec> spec = new ArrayList<>();
            List<Object> input = (List<Object>) c.get("input");
            spec = parseMultiSpec((List<Object>) input.get(0));
            List<Integer> actual = flattenRepr(new Solution().flatten(buildLevel(spec)));
            int[] expectedRaw = Common.toIntArray((List<Object>) c.get("expected"));
            List<Integer> expected = new ArrayList<>();
            for (int value : expectedRaw) expected.add(value);
            if (!actual.equals(expected)) {
                Common.reportWA(i, raw, expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }

    @SuppressWarnings("unchecked")
    static List<MultiSpec> parseMultiSpec(List<Object> raw) {
        List<MultiSpec> out = new ArrayList<>();
        for (Object itemObj : raw) {
            Map<String, Object> item = (Map<String, Object>) itemObj;
            MultiSpec spec = new MultiSpec();
            spec.val = Common.toInt(item.get("val"));
            Object child = item.get("child");
            if (child instanceof List) spec.child = parseMultiSpec((List<Object>) child);
            else spec.child = new ArrayList<>();
            out.add(spec);
        }
        return out;
    }
}
