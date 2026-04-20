import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("subarray-sum-equals-k");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();

        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int arg1 = Common.toInt(input.get(1));
            int expected = Common.toInt(c.get("expected"));

            Solution sol = new Solution();
            int result = sol.subarraySum(arg0.clone(), arg1);

            if (result != expected) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected), String.valueOf(result), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
