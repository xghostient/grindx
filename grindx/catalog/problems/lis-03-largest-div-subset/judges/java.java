import java.util.*;


class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("lis-03-largest-div-subset");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[] arr = Common.toIntArray((List<Object>) input.get(0));
    int[] actual = new Solution().largestDivisibleSubset(arr);
    int expected = Common.toInt(c.get("expected"));
    Set<Integer> inputSet = new HashSet<>();
    for (int value : arr) inputSet.add(value);
    Set<Integer> actualSet = new HashSet<>();
    boolean valid = actual.length == expected;
    if (valid) {
        for (int value : actual) {
            if (actualSet.contains(value) || !inputSet.contains(value)) valid = false;
            actualSet.add(value);
        }
    }
    if (valid) {
        for (int x = 0; x < actual.length; x++) {
            for (int y = x + 1; y < actual.length; y++) {
                if (actual[x] % actual[y] != 0 && actual[y] % actual[x] != 0) valid = false;
            }
        }
    }
    if (!valid) {
        Common.reportWA(i, input, "valid divisible subset length " + expected, Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
    }
            Common.reportProgress(i + 1, total);
}

        Common.reportAC(total);
    }
}
