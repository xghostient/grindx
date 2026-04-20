import java.util.*;

class Judge {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("rotate-image");
    List<Object> cases = (List<Object>) tc.get("cases");
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[][] arg0 = Common.toIntMatrix((List<Object>) input.get(0));
            int[][] expected = Common.toIntMatrix((List<Object>) c.get("expected"));

                    Solution sol = new Solution();
                    sol.rotate(arg0);
                    var actual = arg0;
            if (!Arrays.deepEquals(actual, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.deepToString(expected), Arrays.deepToString(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
