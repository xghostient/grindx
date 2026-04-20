        import java.util.*;

        class Judge {
        static int[] toIntArray(List<Object> raw) {
    int[] out = new int[raw.size()];
    for (int i = 0; i < raw.size(); i++) out[i] = ((Number) raw.get(i)).intValue();
    return out;
}

static List<String> toStringList(List<Object> raw) {
    List<String> out = new ArrayList<>();
    for (Object value : raw) out.add(String.valueOf(value));
    return out;
}

static List<String> sortedStrings(List<String> raw) {
    List<String> out = new ArrayList<>(raw);
    Collections.sort(out);
    return out;
}

@SuppressWarnings("unchecked")
static List<String> normalizeStringResult(Object raw) {
    if (raw instanceof String[]) {
        return sortedStrings(Arrays.asList((String[]) raw));
    }
    if (raw instanceof List<?>) {
        List<String> out = new ArrayList<>();
        for (Object value : (List<Object>) raw) out.add(String.valueOf(value));
        return sortedStrings(out);
    }
    return new ArrayList<>();
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("next-greater-element-ii");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] nums = toIntArray((List<Object>) input.get(0));
    int[] actual = new Solution().nextGreaterElements(nums);
    int[] expected = toIntArray((List<Object>) c.get("expected"));
    if (!Arrays.equals(actual, expected)) Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
