import java.util.*;

class Judge {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("valid-sudoku");
    List<Object> cases = (List<Object>) tc.get("cases");
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            char[][] arg0 = Common.toCharMatrix((List<Object>) input.get(0));
            boolean expected = (Boolean) c.get("expected");

                    Solution sol = new Solution();
                    boolean result = sol.isValidSudoku(arg0);
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
