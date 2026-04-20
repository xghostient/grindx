        import java.util.*;

        class Judge {
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
                Map<String, Object> tc = Common.loadCases("merge-sorted-array");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] nums1 = toIntArray(input.get(0));
    int m = Common.toInt(input.get(1));
    int[] nums2 = toIntArray(input.get(2));
    int n = Common.toInt(input.get(3));
    new Solution().merge(nums1, m, nums2, n);
    int[] expected = toIntArray(c.get("expected"));
    if (!Arrays.equals(nums1, expected)) Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(nums1), total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
