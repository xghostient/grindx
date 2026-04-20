import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("mcm-02-min-cost-to-cut-stick");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int n = Common.toInt(input.get(0));
    int[] cuts = Common.toIntArray((List<Object>) input.get(1));
    int actual = new Solution().minCost(n, cuts);
    int expected = Common.toInt(c.get("expected"));
    if (actual != expected) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
            Common.reportProgress(i + 1, total);
}

        Common.reportAC(total);
    }
}
