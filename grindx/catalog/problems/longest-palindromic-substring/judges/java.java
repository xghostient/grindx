        import java.util.*;

        class Judge {
        @SuppressWarnings("unchecked")
static String[] toStringArray(List<Object> raw) {
    String[] out = new String[raw.size()];
    for (int i = 0; i < raw.size(); i++) out[i] = String.valueOf(raw.get(i));
    return out;
}

@SuppressWarnings("unchecked")
static String[][] toStringMatrix(List<Object> raw) {
    String[][] out = new String[raw.size()][];
    for (int i = 0; i < raw.size(); i++) {
        List<Object> row = (List<Object>) raw.get(i);
        out[i] = new String[row.size()];
        for (int j = 0; j < row.size(); j++) out[i][j] = String.valueOf(row.get(j));
    }
    return out;
}

static List<List<String>> normalizeStringGroups(String[][] raw) {
    List<List<String>> result = new ArrayList<>();
    if (raw == null) return result;
    for (String[] row : raw) {
        List<String> group = new ArrayList<>(Arrays.asList(row));
        Collections.sort(group);
        result.add(group);
    }
    result.sort(Comparator.comparing(Object::toString));
    return result;
}

static List<List<String>> normalizeStringGroups(List<List<String>> raw) {
    List<List<String>> result = new ArrayList<>();
    if (raw == null) return result;
    for (List<String> row : raw) {
        List<String> group = new ArrayList<>(row);
        Collections.sort(group);
        result.add(group);
    }
    result.sort(Comparator.comparing(Object::toString));
    return result;
}

@SuppressWarnings("unchecked")
static List<List<String>> normalizeRawStringGroups(List<Object> raw) {
    List<List<String>> result = new ArrayList<>();
    for (Object rowObj : raw) {
        List<Object> row = (List<Object>) rowObj;
        List<String> group = new ArrayList<>(row.size());
        for (Object item : row) group.add(String.valueOf(item));
        Collections.sort(group);
        result.add(group);
    }
    result.sort(Comparator.comparing(Object::toString));
    return result;
}

static String[] deriveProbeStrings(String[] strs) {
    String[] out = Arrays.copyOf(strs, strs.length + 1);
    for (int i = 0; i < strs.length; i++) out[i] = strs[i] + "#probe";
    out[strs.length] = "|probe|";
    return out;
}

        static boolean isValidLongestPalindrome(String source, String expected, String actual) {
    if (actual == null || actual.length() != expected.length()) return false;
    if (!source.contains(actual)) return false;
    for (int i = 0, j = actual.length() - 1; i < j; i++, j--) {
        if (actual.charAt(i) != actual.charAt(j)) return false;
    }
    return true;
}

static boolean isValidFrequencySort(String source, String actual) {
    if (actual == null || source.length() != actual.length()) return false;
    Map<Character, Integer> counts = new HashMap<>();
    Map<Character, Integer> seen = new HashMap<>();
    for (int i = 0; i < source.length(); i++) counts.merge(source.charAt(i), 1, Integer::sum);
    for (int i = 0; i < actual.length(); i++) seen.merge(actual.charAt(i), 1, Integer::sum);
    if (!counts.equals(seen)) return false;
    for (int i = 1; i < actual.length(); i++) {
        if (counts.get(actual.charAt(i - 1)) < counts.get(actual.charAt(i))) return false;
    }
    return true;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("longest-palindromic-substring");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    String s = String.valueOf(input.get(0));
    String actual = new Solution().longestPalindrome(s);
    String expected = String.valueOf(c.get("expected"));
    if (!isValidLongestPalindrome(s, expected, actual)) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
