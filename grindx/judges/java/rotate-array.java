import java.util.*;

/**
 * Judge for Rotate Array — in-place mutation pattern.
 */
class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("rotate-array");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<Object[]> largeCases = generateLargeCases();
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
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            Object[] lc = largeCases.get(li);
            int[] nums = (int[]) lc[0];
            int k = (int) lc[1];
            int[] expected = (int[]) lc[2];

            int[] numsClone = nums.clone();
            Solution sol = new Solution();
            sol.rotate(numsClone, k);

            if (!Arrays.equals(numsClone, expected)) {
                Common.reportWA(idx, "large input (" + nums.length + " elements)",
                    Common.truncate(Arrays.toString(expected), 200),
                    Common.truncate(Arrays.toString(numsClone), 200), total, "tle");
            }
        }

        Common.reportAC(total);
    }

    private static List<Object[]> generateLargeCases() {
        List<Object[]> cases = new ArrayList<>();
        Random rng = new Random(42);
        int n = 100000;

        // Large case 1: k < n
        {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = rng.nextInt(2000000001) - 1000000000;
            }
            int k = rng.nextInt(n);
            int[] expected = computeExpected(nums, k);
            cases.add(new Object[]{nums, k, expected});
        }

        // Large case 2: k > n
        {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = rng.nextInt(2000000001) - 1000000000;
            }
            int k = n + rng.nextInt(n);
            int[] expected = computeExpected(nums, k);
            cases.add(new Object[]{nums, k, expected});
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
