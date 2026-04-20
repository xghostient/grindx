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
                Map<String, Object> tc = Common.loadCases("pow-x-n");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
                    Map<String, Object> c = (Map<String, Object>) cases.get(i);
                    List<Object> input = (List<Object>) c.get("input");
                    double actual = new Solution().myPow(((Number) input.get(0)).doubleValue(), Common.toInt(input.get(1)));
                    double expected = ((Number) c.get("expected")).doubleValue();
                    double diff = Math.abs(actual - expected);
                    boolean pass = Double.isFinite(actual) && (diff <= 1e-5 || diff / Math.max(Math.abs(expected), 1e-9) <= 1e-5);
                    if (!pass) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
                    Common.reportProgress(i + 1, total);
                }
                Common.reportAC(total);
            }
        }
