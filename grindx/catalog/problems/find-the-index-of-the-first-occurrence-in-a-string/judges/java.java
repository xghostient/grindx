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


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("find-the-index-of-the-first-occurrence-in-a-string");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    String s = String.valueOf(input.get(0));
    String t = String.valueOf(input.get(1));
    int actual = new Solution().strStr(s, t);
    int expected = Common.toInt(c.get("expected"));
    if (actual != expected) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
