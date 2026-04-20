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
                Map<String, Object> tc = Common.loadCases("heap-sort");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
                    Map<String, Object> c = (Map<String, Object>) cases.get(i);
                    List<Object> input = (List<Object>) c.get("input");
                    int[] actual = new Solution().heapSort(toIntArray(input.get(0)));
                    List<Integer> expected = toIntList(c.get("expected"));
                    List<Integer> actualNorm = Arrays.stream(actual).boxed().toList();
                    if (!actualNorm.equals(expected)) Common.reportWA(i, input, expected, actualNorm, total, (String) c.getOrDefault("category", ""));
                    Common.reportProgress(i + 1, total);
                }
                Common.reportAC(total);
            }
        }
