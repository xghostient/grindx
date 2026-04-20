import java.util.*;

class Judge {
private static Map<String, Object> buildLargeCase(int n, int missing, int repeating) {
    int[] input = new int[n];
    for (int i = 0; i < n; i++) input[i] = i + 1;
    input[missing - 1] = repeating;

    Map<String, Object> c = new HashMap<>();
    List<Object> wrappedInput = new ArrayList<>();
    List<Object> inputList = new ArrayList<>(input.length);
    for (int value : input) inputList.add(value);
    wrappedInput.add(inputList);

    List<Object> expected = new ArrayList<>(2);
    expected.add(repeating);
    expected.add(missing);
    c.put("input", wrappedInput);
    c.put("expected", expected);
    c.put("category", "stress");
    return c;
}

private static List<Map<String, Object>> generateLargeCases() {
    int n = 100000;
    return List.of(
        buildLargeCase(n, 1, n),
        buildLargeCase(n, n, n / 2),
        buildLargeCase(n, 42424, 99999)
    );
}

@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("missing-repeating");
    List<Object> cases = new ArrayList<>((List<Object>) tc.get("cases"));
    cases.addAll(generateLargeCases());
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int[] expected = Common.toIntArray((List<Object>) c.get("expected"));

                    Solution sol = new Solution();
                    int[] result = sol.findMissingRepeating(arg0);
                    var actual = result;
            if (!Arrays.equals(actual, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
