import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("product-of-array-except-self");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();

        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int[] expected = Common.toIntArray((List<Object>) c.get("expected"));

            Solution sol = new Solution();
            int[] result = sol.productExceptSelf(arg0.clone());

            if (!Arrays.equals(result, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(result), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
