import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("word-break");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    String s = String.valueOf(input.get(0));
    List<Object> rawWords = (List<Object>) input.get(1);
    String[] words = new String[rawWords.size()];
    for (int j = 0; j < rawWords.size(); j++) {
        words[j] = String.valueOf(rawWords.get(j));
    }
    boolean actual = new Solution().wordBreak(s, words);
    boolean expected = (Boolean) c.get("expected");
    if (actual != expected) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
            Common.reportProgress(i + 1, total);
}

        Common.reportAC(total);
    }
}
