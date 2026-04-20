import java.util.*;

class Judge {
    private static List<List<Integer>> normalizeNested(int[][] values) {
        List<List<Integer>> result = new ArrayList<>();
        for (int[] row : values) {
            List<Integer> current = new ArrayList<>();
            for (int value : row) {
                current.add(value);
            }
            Collections.sort(current);
            result.add(current);
        }
        result.sort(Comparator.comparing(Object::toString));
        return result;
    }
@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("combination-sum");
    List<Object> cases = (List<Object>) tc.get("cases");
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int arg1 = Common.toInt(input.get(1));
            List<List<Integer>> expected = Common.normalizeNestedIntLists((List<Object>) c.get("expected"));

                    Solution sol = new Solution();
                    int[][] result = sol.combinationSum(arg0, arg1);
                    var actual = normalizeNested(result);
            if (!actual.equals(expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected), String.valueOf(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
