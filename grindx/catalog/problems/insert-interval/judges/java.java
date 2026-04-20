        import java.util.*;

        class Judge {
        static int[] toIntArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    int[] out = new int[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = Common.toInt(values.get(i));
    return out;
}

static int[][] toIntMatrix(Object raw) {
    List<Object> rows = (List<Object>) raw;
    int[][] out = new int[rows.size()][];
    for (int i = 0; i < rows.size(); i++) out[i] = toIntArray(rows.get(i));
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("insert-interval");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[][] intervals = toIntMatrix(input.get(0));
    int[] newInterval = toIntArray(input.get(1));
    int[][] actual = new Solution().insert(intervals, newInterval);
    if (actual == null) actual = new int[0][];
    int[][] expected = toIntMatrix(c.get("expected"));
    if (!Arrays.deepEquals(actual, expected)) Common.reportWA(i, input, Arrays.deepToString(expected), Arrays.deepToString(actual), total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
