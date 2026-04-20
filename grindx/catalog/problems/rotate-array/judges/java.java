import java.util.*;

/**
 * Judge for Rotate Array — in-place mutation pattern.
 */
class Judge {
    private static final class LargeCase {
        final int[] nums;
        final int k;
        final int[] expected;

        LargeCase(int[] nums, int k, int[] expected) {
            this.nums = nums;
            this.k = k;
            this.expected = expected;
        }
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("rotate-array");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<LargeCase> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] nums = Common.toIntArray((List<Object>) input.get(0));
            int k = Common.toInt(input.get(1));

            int[] numsClone = nums.clone();
            Solution sol = new Solution();
            sol.rotate(numsClone, k);

            int[] expected = Common.toIntArray((List<Object>) c.get("expected"));

            if (!Arrays.equals(numsClone, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected),
                    Arrays.toString(numsClone), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            LargeCase lc = largeCases.get(li);

            int[] numsClone = lc.nums.clone();
            Solution sol = new Solution();
            sol.rotate(numsClone, lc.k);

            if (!Arrays.equals(numsClone, lc.expected)) {
                Common.reportWA(idx, "large input (" + lc.nums.length + " elements)",
                    Common.truncate(Arrays.toString(lc.expected), 200),
                    Common.truncate(Arrays.toString(numsClone), 200), total, "tle");
            }
        }

        Common.reportAC(total);
    }

    private static List<LargeCase> generateLargeCases() {
        List<LargeCase> cases = new ArrayList<>();
        for (int[] spec : new int[][]{
            {100000, 99999, -1000000000, 37},
            {100000, 87500, -999900000, 53},
            {100000, 75000, -999800000, 61},
            {100000, 62500, -999700000, 73},
            {100000, 50000, -999600000, 79},
            {100000, 37500, -999500000, 83},
            {100000, 25000, -999400000, 89},
            {99999, 99998, -999300000, 97},
        }) {
            int n = spec[0];
            int k = spec[1];
            int start = spec[2];
            int step = spec[3];
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = start + (i * step);
            }
            cases.add(new LargeCase(nums, k, computeExpected(nums, k)));
        }
        return cases;
    }

    private static int[] computeExpected(int[] nums, int k) {
        int n = nums.length;
        int ek = k % n;
        int[] expected = new int[n];
        for (int i = 0; i < n; i++) {
            expected[(i + ek) % n] = nums[i];
        }
        return expected;
    }
}
