import java.util.*;

class Judge {
    static class Built {
        Node head;
        List<Node> nodes;
        Built(Node head, List<Node> nodes) {
            this.head = head;
            this.nodes = nodes;
        }
    }

    @SuppressWarnings("unchecked")
    static Built buildRandom(List<Object> spec) {
        if (spec.isEmpty()) return new Built(null, new ArrayList<>());
        List<Node> nodes = new ArrayList<>();
        for (Object itemObj : spec) {
            List<Object> item = (List<Object>) itemObj;
            nodes.add(new Node(Common.toInt(item.get(0))));
        }
        for (int i = 0; i + 1 < nodes.size(); i++) nodes.get(i).next = nodes.get(i + 1);
        for (int i = 0; i < nodes.size(); i++) {
            List<Object> item = (List<Object>) spec.get(i);
            if (item.get(1) != null) nodes.get(i).random = nodes.get(Common.toInt(item.get(1)));
        }
        return new Built(nodes.get(0), nodes);
    }

    static List<List<Object>> randomRepr(Node head) {
        List<Node> nodes = new ArrayList<>();
        Map<Node, Integer> index = new IdentityHashMap<>();
        for (Node cur = head; cur != null; cur = cur.next) {
            index.put(cur, nodes.size());
            nodes.add(cur);
        }
        List<List<Object>> out = new ArrayList<>();
        for (Node node : nodes) {
            out.add(Arrays.asList(node.val, node.random == null ? null : index.get(node.random)));
        }
        return out;
    }

    static boolean containsNode(List<Node> nodes, Node target) {
        for (Node node : nodes) if (node == target) return true;
        return false;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("copy-list-with-random-pointer");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> spec = (List<Object>) ((List<Object>) c.get("input")).get(0);
            if (spec.size() == 1 && spec.get(0) instanceof List && ((List<?>) spec.get(0)).isEmpty()) spec = new ArrayList<>();
            Built built = buildRandom(spec);
            Node result = new Solution().copyRandomList(built.head);
            boolean deepOk = true;
            for (Node cur = result; cur != null; cur = cur.next) {
                if (containsNode(built.nodes, cur)) {
                    deepOk = false;
                    break;
                }
            }
            List<List<Object>> actual = randomRepr(result);
            List<List<Object>> expected = (List<List<Object>>) c.get("expected");
            if (!actual.equals(expected) || !deepOk) {
                Common.reportWA(i, c.get("input"), expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
