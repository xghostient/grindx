import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("find-the-duplicate-number");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            int actual = new Solution().findDuplicate(Common.toIntArray((List<Object>) ((List<Object>) c.get("input")).get(0)));
            int expected = Common.toInt(c.get("expected"));
            if (actual != expected) {
                Common.reportWA(i, c.get("input"), expected, actual, total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
