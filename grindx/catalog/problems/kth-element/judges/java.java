import java.util.*;

class Judge {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("kth-element");
    List<Object> cases = (List<Object>) tc.get("cases");
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int[] arg1 = Common.toIntArray((List<Object>) input.get(1));
            int arg2 = Common.toInt(input.get(2));
            int expected = Common.toInt(c.get("expected"));

                    Solution sol = new Solution();
                    int result = sol.kthElement(arg0, arg1, arg2);
                    var actual = result;
            if (actual != expected) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected), String.valueOf(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
