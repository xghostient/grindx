import java.util.*;

class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("dp-on-tries-min-valid-substring");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            String s = String.valueOf(input.get(0));
            List<Object> rawDict = (List<Object>) input.get(1);
            String[] dictionary = new String[rawDict.size()];
            for (int k = 0; k < rawDict.size(); k++) dictionary[k] = String.valueOf(rawDict.get(k));
            int actual = new Solution().minExtraChar(s, dictionary);
            int expected = Common.toInt(c.get("expected"));
            if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
