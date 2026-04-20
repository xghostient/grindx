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
                Map<String, Object> tc = Common.loadCases("reverse-stack");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] stackArr = toIntArray(input.get(0));
    java.util.Stack<Integer> stack = new java.util.Stack<>();
    for (int v : stackArr) stack.push(v);
    new Solution().reverseStack(stack);
    int[] actual = new int[stack.size()];
    for (int j = 0; j < actual.length; j++) actual[j] = stack.get(j);
    int[] expected = toIntArray(c.get("expected"));
    if (!Arrays.equals(actual, expected)) Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
