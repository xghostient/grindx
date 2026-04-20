import java.util.*;

class Judge {
private static List<Map<String, Object>> generateLargeCases() {
    List<Map<String, Object>> out = new ArrayList<>();

    int[] stressOne = new int[50000];
    for (int i = 0; i < 16666; i++) stressOne[i] = i + 3;
    for (int i = 16666; i < 33333; i++) stressOne[i] = 1;
    for (int i = 33333; i < 50000; i++) stressOne[i] = 2;

    int[] stressTwo = new int[50000];
    for (int i = 0; i < 33333; i++) stressTwo[i] = i + 2;
    for (int i = 33333; i < 50000; i++) stressTwo[i] = 1;

    int[] stressThree = new int[50000];
    for (int i = 0; i < 16666; i++) stressThree[i] = -(i + 3);
    for (int i = 16666; i < 33333; i++) stressThree[i] = -1;
    for (int i = 33333; i < 50000; i++) stressThree[i] = -2;

    int[] stressFour = new int[50000];
    for (int i = 0; i < 33333; i++) stressFour[i] = 1_000_000_000 - i;
    for (int i = 33333; i < 50000; i++) stressFour[i] = 999_999_999;

    int[] stressFive = new int[50000];
    for (int i = 0; i < 16666; i++) stressFive[i] = 500_000_000 + i;
    for (int i = 16666; i < 33333; i++) stressFive[i] = 7;
    for (int i = 33333; i < 50000; i++) stressFive[i] = 8;

    int[] stressSix = new int[50000];
    for (int i = 0; i < 33333; i++) stressSix[i] = -(500_000_000 + i);
    for (int i = 33333; i < 50000; i++) stressSix[i] = -7;

    int[] stressSeven = new int[50000];
    for (int i = 0; i < 16666; i++) stressSeven[i] = 250_000_000 + i;
    for (int i = 16666; i < 33333; i++) stressSeven[i] = 123_456_789;
    for (int i = 33333; i < 50000; i++) stressSeven[i] = 987_654_321;

    int[] stressEight = new int[50000];
    for (int i = 0; i < 33333; i++) stressEight[i] = -(250_000_000 + i);
    for (int i = 33333; i < 50000; i++) stressEight[i] = -123_456_789;

    out.add(makeCase(stressOne, new int[]{1, 2}));
    out.add(makeCase(stressTwo, new int[]{1}));
    out.add(makeCase(stressThree, new int[]{-2, -1}));
    out.add(makeCase(stressFour, new int[]{999_999_999}));
    out.add(makeCase(stressFive, new int[]{7, 8}));
    out.add(makeCase(stressSix, new int[]{-7}));
    out.add(makeCase(stressSeven, new int[]{123_456_789, 987_654_321}));
    out.add(makeCase(stressEight, new int[]{-123_456_789}));
    List<Map<String, Object>> repeated = new ArrayList<>(out.size() * 4);
    for (int rep = 0; rep < 4; rep++) repeated.addAll(out);
    return repeated;
}

private static Map<String, Object> makeCase(int[] input, int[] expected) {
    Map<String, Object> c = new HashMap<>();
    List<Object> wrappedInput = new ArrayList<>();
    List<Object> inputList = new ArrayList<>(input.length);
    for (int value : input) inputList.add(value);
    wrappedInput.add(inputList);
    List<Object> expectedList = new ArrayList<>(expected.length);
    for (int value : expected) expectedList.add(value);
    c.put("input", wrappedInput);
    c.put("expected", expectedList);
    c.put("category", "stress");
    return c;
}

private static boolean unorderedEqual(int[] actual, int[] expected) {
    int[] a = Arrays.copyOf(actual, actual.length);
    int[] e = Arrays.copyOf(expected, expected.length);
    Arrays.sort(a);
    Arrays.sort(e);
    return Arrays.equals(a, e);
}

@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("majority-element-2");
    List<Object> cases = new ArrayList<>((List<Object>) tc.get("cases"));
    cases.addAll(generateLargeCases());
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int[] expected = Common.toIntArray((List<Object>) c.get("expected"));

                    Solution sol = new Solution();
                    int[] result = sol.majorityElement(arg0);
                    int[] actual = result != null ? result : new int[0];
            if (!unorderedEqual(actual, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        Common.reportAC(total);
    }
}
