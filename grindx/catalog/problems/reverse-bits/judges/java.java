        import java.util.*;

        class Judge {
        static int[] toIntArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    int[] out = new int[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = Common.toInt(values.get(i));
    return out;
}

            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("reverse-bits");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            long x = ((Number) input.get(0)).longValue();
            long actual = new Solution().reverseBits(x);
            long expected = ((Number) c.get("expected")).longValue();
            if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
                Common.reportAC(total);
            }
        }
