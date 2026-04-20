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

        static int badVersion = 0;
static boolean isBadVersion(int version) {
    return version >= badVersion;
}

            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("first-bad-version");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            List<Object> pair = (List<Object>) input.get(0);
            int n = Common.toInt(pair.get(0));
            int bad = Common.toInt(pair.get(1));
            Judge.badVersion = bad;
            int actual = new Solution().firstBadVersion(n);
            int expected = Common.toInt(c.get("expected"));
            if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
                Common.reportAC(total);
            }
        }
