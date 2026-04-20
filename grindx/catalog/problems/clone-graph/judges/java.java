        import java.util.*;

        class Judge {
        static int[][] cloneMatrix(int[][] matrix) {
    int[][] out = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) {
        out[i] = Arrays.copyOf(matrix[i], matrix[i].length);
    }
    return out;
}

static char[][] stringRowsToGrid(List<Object> rows) {
    return Common.toCharMatrix(rows);
}

static List<String> gridToStringRows(char[][] board) {
    List<String> result = new ArrayList<>();
    for (char[] row : board) {
        result.add(new String(row));
    }
    return result;
}

static Node adjListToGraph(List<Object> raw) {
    if (raw.isEmpty()) return null;
    Node[] nodes = new Node[raw.size() + 1];
    for (int i = 1; i <= raw.size(); i++) {
        nodes[i] = new Node(i);
    }
    for (int i = 0; i < raw.size(); i++) {
        List<Object> row = (List<Object>) raw.get(i);
        Node[] neighbors = new Node[row.size()];
        for (int j = 0; j < row.size(); j++) {
            neighbors[j] = nodes[Common.toInt(row.get(j))];
        }
        nodes[i + 1].neighbors = neighbors;
    }
    return nodes[1];
}

static List<List<Integer>> graphToAdjList(Node node) {
    List<List<Integer>> result = new ArrayList<>();
    if (node == null) return result;
    Map<Integer, Node> visited = new HashMap<>();
    Queue<Node> queue = new ArrayDeque<>();
    visited.put(node.val, node);
    queue.add(node);
    while (!queue.isEmpty()) {
        Node current = queue.poll();
        for (Node neighbor : current.neighbors) {
            if (!visited.containsKey(neighbor.val)) {
                visited.put(neighbor.val, neighbor);
                queue.add(neighbor);
            }
        }
    }
    int maxVal = Collections.max(visited.keySet());
    for (int value = 1; value <= maxVal; value++) {
        List<Integer> row = new ArrayList<>();
        if (visited.containsKey(value)) {
            for (Node neighbor : visited.get(value).neighbors) {
                row.add(neighbor.val);
            }
            Collections.sort(row);
        }
        result.add(row);
    }
    return result;
}

static boolean graphSharesIdentity(Node original, Node clone) {
    if (original == null || clone == null) return false;
    Set<Node> originalNodes = new HashSet<>();
    Queue<Node> queue = new ArrayDeque<>();
    queue.add(original);
    while (!queue.isEmpty()) {
        Node current = queue.poll();
        if (!originalNodes.add(current)) continue;
        queue.addAll(Arrays.asList(current.neighbors));
    }
    Set<Node> seen = new HashSet<>();
    queue.add(clone);
    while (!queue.isEmpty()) {
        Node current = queue.poll();
        if (!seen.add(current)) continue;
        if (originalNodes.contains(current)) return true;
        queue.addAll(Arrays.asList(current.neighbors));
    }
    return false;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("clone-graph");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    Node graph = adjListToGraph((List<Object>) input.get(0));
    Node cloned = new Solution().cloneGraph(graph);
    if (graphSharesIdentity(graph, cloned)) {
        Common.reportWA(i, input, "deep copy without shared nodes", "shared original nodes", total, (String) c.getOrDefault("category", ""));
    }
    List<List<Integer>> actual = graphToAdjList(cloned);
    List<List<Integer>> expected = Common.normalizeNestedIntLists((List<Object>) c.get("expected"));
    if (!actual.equals(expected)) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
