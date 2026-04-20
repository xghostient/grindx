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
                Map<String, Object> tc = Common.loadCases("plus-one");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
                    Map<String, Object> c = (Map<String, Object>) cases.get(i);
                    List<Object> input = (List<Object>) c.get("input");
                    int[] actual = new Solution().plusOne(toIntArray(input.get(0)));
                    List<Integer> expected = toIntList(c.get("expected"));
                    List<Integer> actualList = new ArrayList<>();
                    for (int v : actual) actualList.add(v);
                    if (!actualList.equals(expected)) Common.reportWA(i, input, expected, actualList, total, (String) c.getOrDefault("category", ""));
                    Common.reportProgress(i + 1, total);
                }
                Common.reportAC(total);
            }
        }
