import java.util.*;

class Judge {
private static List<Map<String, Object>> generateLargeCases() {
    List<Map<String, Object>> out = new ArrayList<>();

    int[] stressOne = new int[50000];
    for (int i = 0; i < 24999; i++) stressOne[i] = i + 2;
    for (int i = 24999; i < 50000; i++) stressOne[i] = 1;

    int[] stressTwo = new int[50000];
    for (int i = 0; i < 24999; i++) stressTwo[i] = -(i + 2);
    for (int i = 24999; i < 50000; i++) stressTwo[i] = -1;

    int[] stressThree = new int[50000];
    for (int i = 0; i < 24999; i++) stressThree[i] = 1_000_000_000 - i;
    for (int i = 24999; i < 50000; i++) stressThree[i] = 999_999_999;

    int[] stressFour = new int[50000];
    for (int i = 0; i < 24999; i++) stressFour[i] = -(1_000_000_000 - i);
    for (int i = 24999; i < 50000; i++) stressFour[i] = -999_999_999;

    int[] stressFive = new int[50000];
    for (int i = 0; i < 24999; i++) stressFive[i] = 500_000_000 + i;
    for (int i = 24999; i < 50000; i++) stressFive[i] = 7;

    int[] stressSix = new int[50000];
    for (int i = 0; i < 24999; i++) stressSix[i] = -(500_000_000 + i);
    for (int i = 24999; i < 50000; i++) stressSix[i] = -7;

    int[] stressSeven = new int[50000];
    for (int i = 0; i < 24999; i++) stressSeven[i] = 250_000_000 + i;
    for (int i = 24999; i < 50000; i++) stressSeven[i] = 123_456_789;

    int[] stressEight = new int[50000];
    for (int i = 0; i < 24999; i++) stressEight[i] = -(250_000_000 + i);
    for (int i = 24999; i < 50000; i++) stressEight[i] = -123_456_789;

    out.add(makeCase(stressOne, 1));
    out.add(makeCase(stressTwo, -1));
    out.add(makeCase(stressThree, 999_999_999));
    out.add(makeCase(stressFour, -999_999_999));
    out.add(makeCase(stressFive, 7));
    out.add(makeCase(stressSix, -7));
    out.add(makeCase(stressSeven, 123_456_789));
    out.add(makeCase(stressEight, -123_456_789));
    List<Map<String, Object>> repeated = new ArrayList<>(out.size() * 4);
    for (int rep = 0; rep < 4; rep++) repeated.addAll(out);
    return repeated;
}

private static Map<String, Object> makeCase(int[] input, int expected) {
    Map<String, Object> c = new HashMap<>();
    List<Object> wrappedInput = new ArrayList<>();
    List<Object> inputList = new ArrayList<>(input.length);
    for (int value : input) inputList.add(value);
    wrappedInput.add(inputList);
    c.put("input", wrappedInput);
    c.put("expected", expected);
    c.put("category", "stress");
    return c;
}

@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("majority-element");
    List<Object> cases = new ArrayList<>((List<Object>) tc.get("cases"));
    cases.addAll(generateLargeCases());
    int total = cases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int expected = Common.toInt(c.get("expected"));

                    Solution sol = new Solution();
                    int result = sol.majorityElement(arg0);
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
