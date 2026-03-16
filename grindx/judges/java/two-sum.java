import java.util.*;

/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */
class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("two-sum");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large cases for TLE detection
        List<int[][]> largeCases = generateLargeCases();
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

            int[] sortedResult = result.clone();
            int[] sortedExpected = expected.clone();
            Arrays.sort(sortedResult);
            Arrays.sort(sortedExpected);

            if (!Arrays.equals(sortedResult, sortedExpected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected),
                    Arrays.toString(result), total, category);
            }
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            int[][] lc = largeCases.get(li);
            int[] nums = lc[0];
            int target = lc[1][0];

            Solution sol = new Solution();
            int[] result = sol.twoSum(nums.clone(), target);

            if (result.length != 2 || result[0] == result[1] ||
                nums[result[0]] + nums[result[1]] != target) {
                Common.reportWA(idx, "large input", target,
                    Arrays.toString(result), total, "tle");
            }
        }

        Common.reportAC(total);
    }

    private static List<int[][]> generateLargeCases() {
        List<int[][]> cases = new ArrayList<>();
        Random rng = new Random(42);
        for (int n : new int[]{10000, 100000}) {
            int[] nums = new int[n];
            for (int k = 0; k < n; k++) {
                nums[k] = rng.nextInt(2000000001) - 1000000000;
            }
            int i = rng.nextInt(n);
            int j = rng.nextInt(n);
            while (j == i) j = (j + 1) % n;
            int target = nums[i] + nums[j];
            cases.add(new int[][]{nums, {target}});
        }
        return cases;
    }
}
