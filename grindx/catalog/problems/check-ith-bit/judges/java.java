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
                Map<String, Object> tc = Common.loadCases("check-ith-bit");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int n = Common.toInt(input.get(0));
            int k = Common.toInt(input.get(1));
            boolean actual = new Solution().checkIthBit(n, k);
            boolean expected = (Boolean) c.get("expected");
            if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
                Common.reportAC(total);
            }
        }
