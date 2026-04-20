        import java.util.*;
import java.util.function.BiFunction;


        class Judge {
            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("print-longest-common-subseq");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                BiFunction<String, String, Boolean> isSubsequence = (needle, haystack) -> {
            int idx = 0;
            for (int pos = 0; pos < haystack.length(); pos++) {
                if (idx < needle.length() && needle.charAt(idx) == haystack.charAt(pos)) idx++;
            }
            return idx == needle.length();
        };

        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            String a = String.valueOf(input.get(0));
            String b = String.valueOf(input.get(1));
            String actual = new Solution().printLCS(a, b);
            int expected = Common.toInt(c.get("expected"));
            if (actual.length() != expected || !isSubsequence.apply(actual, a) || !isSubsequence.apply(actual, b)) {
                Common.reportWA(i, input, "valid LCS length " + expected, actual, total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }

                Common.reportAC(total);
            }
        }
