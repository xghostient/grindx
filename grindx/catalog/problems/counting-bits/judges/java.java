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
                Map<String, Object> tc = Common.loadCases("counting-bits");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int n = Common.toInt(input.get(0));
            int[] actual = new Solution().countBits(n);
            int[] expected = toIntArray(c.get("expected"));
            if (!Arrays.equals(actual, expected)) Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
                Common.reportAC(total);
            }
        }
