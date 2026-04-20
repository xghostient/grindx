import java.util.*;

class Judge {
private static final class LargeCase {
    final int[] customers;
    final int[] grumpy;
    final int minutes;
    final int expected;

    LargeCase(int[] customers, int[] grumpy, int minutes, int expected) {
        this.customers = customers;
        this.grumpy = grumpy;
        this.minutes = minutes;
        this.expected = expected;
    }
}

private static int expected(int[] customers, int[] grumpy, int minutes) {
    int base = 0;
    for (int i = 0; i < customers.length; i++) {
        if (grumpy[i] == 0) base += customers[i];
    }
    int extra = 0;
    for (int i = 0; i < minutes; i++) {
        if (grumpy[i] == 1) extra += customers[i];
    }
    int best = extra;
    for (int i = minutes; i < customers.length; i++) {
        if (grumpy[i] == 1) extra += customers[i];
        if (grumpy[i - minutes] == 1) extra -= customers[i - minutes];
        if (extra > best) best = extra;
    }
    return base + best;
}

private static List<LargeCase> generateLargeCases() {
    int n = 20000;
    ArrayList<LargeCase> cases = new ArrayList<>(32);
    for (int shift = 0; shift < 8; shift++) {
        int[] customers = new int[n];
        int[] grumpy = new int[n];
        for (int i = 0; i < n; i++) {
            customers[i] = (i + shift) % 2 == 0 ? 1000 : 1;
            grumpy[i] = 1;
        }
        int minutes = n / 2 + (shift % 5);
        cases.add(new LargeCase(customers, grumpy, minutes, expected(customers, grumpy, minutes)));
    }
    for (int shift = 0; shift < 8; shift++) {
        int[] customers = new int[n];
        int[] grumpy = new int[n];
        for (int i = 0; i < n; i++) {
            customers[i] = ((i + shift) % 9) * 111;
            grumpy[i] = (i + shift) % 3 == 0 ? 1 : 0;
        }
        int minutes = n / 2 + (shift % 7);
        cases.add(new LargeCase(customers, grumpy, minutes, expected(customers, grumpy, minutes)));
    }
    for (int shift = 0; shift < 8; shift++) {
        int[] customers = new int[n];
        int[] grumpy = new int[n];
        for (int i = 0; i < n; i++) {
            customers[i] = (i + shift) % 4 < 2 ? 5 : 20;
            grumpy[i] = (i + shift) % 5 != 0 ? 1 : 0;
        }
        int minutes = n / 3 + (shift % 11);
        cases.add(new LargeCase(customers, grumpy, minutes, expected(customers, grumpy, minutes)));
    }
    for (int shift = 0; shift < 8; shift++) {
        int[] customers = new int[n];
        int[] grumpy = new int[n];
        for (int i = 0; i < n; i++) {
            customers[i] = 997 - ((i + shift) % 11);
            grumpy[i] = (i + shift) % 2 == 0 ? 1 : 0;
        }
        int minutes = n - 123 - (shift % 17);
        cases.add(new LargeCase(customers, grumpy, minutes, expected(customers, grumpy, minutes)));
    }
    return cases;
}

@SuppressWarnings("unchecked")
public static void main(String[] args) {
    Map<String, Object> tc = Common.loadCases("grumpy-bookstore-owner");
    List<Object> cases = (List<Object>) tc.get("cases");
    List<LargeCase> largeCases = generateLargeCases();
    int total = cases.size() + largeCases.size();

    for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
            int[] arg0 = Common.toIntArray((List<Object>) input.get(0));
            int[] arg1 = Common.toIntArray((List<Object>) input.get(1));
            int arg2 = Common.toInt(input.get(2));
            int expected = Common.toInt(c.get("expected"));

                    Solution sol = new Solution();
                    int result = sol.maxSatisfied(arg0, arg1, arg2);
                    var actual = result;
            if (actual != expected) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, String.valueOf(expected), String.valueOf(actual), total, category);
            }
        Common.reportProgress(i + 1, total);
        }

        for (int li = 0; li < largeCases.size(); li++) {
            LargeCase c = largeCases.get(li);
            Solution sol = new Solution();
            int actual = sol.maxSatisfied(c.customers.clone(), c.grumpy.clone(), c.minutes);
            if (actual != c.expected) {
                Common.reportWA(cases.size() + li, "large input", String.valueOf(c.expected), String.valueOf(actual), total, "tle");
            }
        }

        Common.reportAC(total);
    }
}
