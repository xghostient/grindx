import java.util.*;

/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */
class Judge {
    private static final class LargeCase {
        final int[] nums;
        final int target;
        final int[] expectedIndices;

        LargeCase(int[] nums, int target, int[] expectedIndices) {
            this.nums = nums;
            this.target = target;
            this.expectedIndices = expectedIndices;
        }
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("two-sum");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<LargeCase> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] nums = Common.toIntArray((List<Object>) input.get(0));
            int target = Common.toInt(input.get(1));

            Solution sol = new Solution();
            int[] result = sol.twoSum(nums.clone(), target);

            int[] expected = Common.toIntArray((List<Object>) c.get("expected"));

            if (!isValidIndexPair(result, nums.length)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected),
                    Arrays.toString(result), total, category);
            }

            int[] sortedResult = result.clone();
            int[] sortedExpected = expected.clone();
            Arrays.sort(sortedResult);
            Arrays.sort(sortedExpected);

            if (!Arrays.equals(sortedResult, sortedExpected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected),
                    Arrays.toString(result), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            LargeCase lc = largeCases.get(li);
            int[] nums = lc.nums;

            Solution sol = new Solution();
            int[] result = sol.twoSum(nums.clone(), lc.target);

            if (!isValidIndexPair(result, nums.length)) {
                Common.reportWA(idx, "large input", Arrays.toString(lc.expectedIndices),
                    Arrays.toString(result), total, "tle");
            }

            int[] sortedResult = result.clone();
            int[] sortedExpected = lc.expectedIndices.clone();
            Arrays.sort(sortedResult);
            Arrays.sort(sortedExpected);

            if (!Arrays.equals(sortedResult, sortedExpected)) {
                Common.reportWA(idx, "large input", Arrays.toString(lc.expectedIndices),
                    Arrays.toString(result), total, "tle");
            }
        }

        Common.reportAC(total);
    }

    private static List<LargeCase> generateLargeCases() {
        List<LargeCase> cases = new ArrayList<>();
        final int n = 10000;

        {
            int[] nums = new int[n];
            nums[0] = -500000000;
            for (int i = 1; i < n - 1; i++) {
                nums[i] = 200000000 + ((i * 7919) % 700000000);
            }
            nums[n - 1] = 123456789;
            cases.add(new LargeCase(nums, -376543211, new int[]{0, n - 1}));
        }

        {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = 300000000 + ((i * 1237) % 600000000);
            }
            int dupI = 137;
            int dupJ = 9862;
            nums[dupI] = 123456789;
            nums[dupJ] = 123456789;
            cases.add(new LargeCase(nums, 246913578, new int[]{dupI, dupJ}));
        }

        {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = 1 + ((i * 48271) % 999999998);
            }
            int lowI = 4000;
            int highI = 7000;
            nums[lowI] = -1000000000;
            nums[highI] = 1000000000;
            cases.add(new LargeCase(nums, 0, new int[]{lowI, highI}));
        }

        {
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = 1 + ((i * 8191) % 999999999);
            }
            int zeroI = 2500;
            int zeroJ = 7500;
            nums[zeroI] = 0;
            nums[zeroJ] = 0;
            cases.add(new LargeCase(nums, 0, new int[]{zeroI, zeroJ}));
        }
        return cases;
    }

    private static boolean isValidIndexPair(int[] result, int size) {
        if (result == null || result.length != 2) {
            return false;
        }
        for (int idx : result) {
            if (idx < 0 || idx >= size) {
                return false;
            }
        }
        return true;
    }
}
