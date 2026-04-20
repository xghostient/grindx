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

static List<List<String>> normalizeStrMatrix(String[][] raw) {
    List<List<String>> rows = new ArrayList<>();
    if (raw == null) return rows;
    for (String[] row : raw) {
        rows.add(Arrays.asList(row));
    }
    rows.sort((a, b) -> {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
            int cmp = a.get(i).compareTo(b.get(i));
            if (cmp != 0) return cmp;
        }
        return Integer.compare(a.size(), b.size());
    });
    return rows;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("n-queens");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int n = Common.toInt(input.get(0));
    List<List<String>> actual = normalizeStrMatrix(new Solution().solveNQueens(n));
    List<List<String>> expected = new ArrayList<>();
    for (Object row : (List<Object>) c.get("expected")) {
        List<String> r = new ArrayList<>();
        for (Object s : (List<Object>) row) r.add(String.valueOf(s));
        expected.add(r);
    }
    if (!actual.equals(expected)) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
