        import java.util.*;

        class Judge {
        static int[] toIntArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    int[] out = new int[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = Common.toInt(values.get(i));
    return out;
}

static List<Integer> toIntList(Object raw) {
    List<Object> values = (List<Object>) raw;
    List<Integer> out = new ArrayList<>();
    for (Object value : values) out.add(Common.toInt(value));
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("m-coloring-problem");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int n = Common.toInt(input.get(0));
    List<Object> rawEdges = (List<Object>) input.get(1);
    int[][] edges = new int[rawEdges.size()][2];
    for (int e = 0; e < rawEdges.size(); e++) {
        List<Object> edge = (List<Object>) rawEdges.get(e);
        edges[e][0] = Common.toInt(edge.get(0));
        edges[e][1] = Common.toInt(edge.get(1));
    }
    int m = Common.toInt(input.get(2));
    boolean actual = new Solution().graphColoring(n, edges, m);
    boolean expected = (Boolean) c.get("expected");
    if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
