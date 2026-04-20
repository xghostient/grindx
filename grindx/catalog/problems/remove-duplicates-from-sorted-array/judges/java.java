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
                Map<String, Object> tc = Common.loadCases("remove-duplicates-from-sorted-array");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] nums = toIntArray(input.get(0));
    int actualK = new Solution().removeDuplicates(nums);
    Map<String, Object> expected = (Map<String, Object>) c.get("expected");
    int expectedK = Common.toInt(expected.get("k"));
    int[] expectedPrefix = toIntArray(expected.get("prefix"));
    int[] actualPrefix = actualK >= 0 && actualK <= nums.length ? Arrays.copyOf(nums, actualK) : new int[0];
    if (actualK != expectedK || !Arrays.equals(actualPrefix, expectedPrefix)) {
        Common.reportWA(i, input, expected, Map.of("k", actualK, "prefix", Arrays.toString(actualPrefix)), total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
