        import java.util.*;
import java.util.function.BiFunction;


        class Judge {
            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("lis-02-print-lis");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                BiFunction<int[], int[], Boolean> isSubsequenceList = (seq, arr) -> {
            int idx = 0;
            for (int value : arr) {
                if (idx < seq.length && seq[idx] == value) idx++;
            }
            return idx == seq.length;
        };

        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            int[] actual = new Solution().printLIS(arr);
            int expected = Common.toInt(c.get("expected"));
            boolean valid = actual.length == expected;
            if (valid) {
                for (int j = 0; j + 1 < actual.length; j++) {
                    if (actual[j] >= actual[j + 1]) valid = false;
                }
                if (valid && !isSubsequenceList.apply(actual, arr)) valid = false;
            }
            if (!valid) {
                Common.reportWA(i, input, "valid LIS length " + expected, Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }

                Common.reportAC(total);
            }
        }
