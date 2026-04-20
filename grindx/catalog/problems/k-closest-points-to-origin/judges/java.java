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

static int[][] toIntMatrix(Object raw) {
    List<Object> rows = (List<Object>) raw;
    int[][] out = new int[rows.size()][];
    for (int i = 0; i < rows.size(); i++) out[i] = toIntArray(rows.get(i));
    return out;
}

static List<List<Integer>> normalizeIntMatrix(int[][] raw) {
    List<List<Integer>> rows = new ArrayList<>();
    if (raw == null) return rows;
    for (int[] row : raw) {
        List<Integer> values = new ArrayList<>();
        for (int value : row) values.add(value);
        Collections.sort(values);
        rows.add(values);
    }
    rows.sort((a, b) -> {
        if (a.size() != b.size()) return Integer.compare(a.size(), b.size());
        for (int i = 0; i < a.size(); i++) {
            int cmp = Integer.compare(a.get(i), b.get(i));
            if (cmp != 0) return cmp;
        }
        return 0;
    });
    return rows;
}

static List<Integer> sortedIntListFromIntArray(int[] raw) {
    List<Integer> out = new ArrayList<>();
    if (raw == null) return out;
    for (int value : raw) out.add(value);
    Collections.sort(out);
    return out;
}

static List<Integer> sortedIntListFromList(List<Integer> raw) {
    List<Integer> out = new ArrayList<>(raw);
    Collections.sort(out);
    return out;
}

static char[] toCharArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    char[] out = new char[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = String.valueOf(values.get(i)).charAt(0);
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("k-closest-points-to-origin");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
                    Map<String, Object> c = (Map<String, Object>) cases.get(i);
                    List<Object> input = (List<Object>) c.get("input");
                    List<List<Integer>> actual = normalizeIntMatrix(new Solution().kClosest(toIntMatrix(input.get(0)), Common.toInt(input.get(1))));
                    List<List<Integer>> expected = new ArrayList<>();
                    for (Object row : (List<Object>) c.get("expected")) expected.add(toIntList(row));
                    if (!actual.equals(expected)) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
                    Common.reportProgress(i + 1, total);
                }
                Common.reportAC(total);
            }
        }
