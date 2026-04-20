        import java.util.*;

        class Judge {
        @SuppressWarnings("unchecked")
static int[] toIntArray(List<Object> raw) {
    int[] out = new int[raw.size()];
    for (int i = 0; i < raw.size(); i++) out[i] = ((Number) raw.get(i)).intValue();
    return out;
}

        static boolean isValidMinWindow(String source, String target, String expected, String actual) {
    if (actual == null || actual.length() != expected.length()) return false;
    if (expected.isEmpty()) return actual.isEmpty();
    if (!source.contains(actual)) return false;
    Map<Character, Integer> need = new HashMap<>();
    Map<Character, Integer> have = new HashMap<>();
    for (int i = 0; i < target.length(); i++) need.merge(target.charAt(i), 1, Integer::sum);
    for (int i = 0; i < actual.length(); i++) have.merge(actual.charAt(i), 1, Integer::sum);
    for (Map.Entry<Character, Integer> entry : need.entrySet()) {
        if (have.getOrDefault(entry.getKey(), 0) < entry.getValue()) return false;
    }
    return true;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("maximum-points-you-can-obtain-from-cards");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] nums = toIntArray((List<Object>) input.get(0));
    int k = Common.toInt(input.get(1));
    int actual = new Solution().maxScore(nums, k);
    int expected = Common.toInt(c.get("expected"));
    if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
