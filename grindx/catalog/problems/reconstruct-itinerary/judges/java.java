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

static List<List<String>> normalizePaths(String[][] paths) {
    List<List<String>> result = new ArrayList<>();
    if (paths == null) return result;
    for (String[] path : paths) result.add(new ArrayList<>(Arrays.asList(path)));
    result.sort(Comparator.comparing(Object::toString));
    return result;
}

static boolean validateAlienOrder(String[] words, String order) {
    Set<Character> chars = new HashSet<>();
    for (String word : words) for (char ch : word.toCharArray()) chars.add(ch);
    if (order == null || order.length() != chars.size()) return false;
    Map<Character, Integer> rank = new HashMap<>();
    for (int i = 0; i < order.length(); i++) {
        char ch = order.charAt(i);
        if (rank.containsKey(ch)) return false;
        rank.put(ch, i);
    }
    if (rank.size() != chars.size()) return false;
    for (char ch : chars) if (!rank.containsKey(ch)) return false;
    for (int i = 0; i + 1 < words.length; i++) {
        String a = words[i], b = words[i + 1];
        int j = 0;
        while (j < a.length() && j < b.length() && a.charAt(j) == b.charAt(j)) j++;
        if (j == Math.min(a.length(), b.length())) {
            if (a.length() > b.length()) return false;
            continue;
        }
        if (rank.get(a.charAt(j)) > rank.get(b.charAt(j))) return false;
    }
    return true;
}


        @SuppressWarnings("unchecked")
        public static void main(String[] args) {
            Map<String, Object> tc = Common.loadCases("reconstruct-itinerary");
            List<Object> cases = (List<Object>) tc.get("cases");
            int total = cases.size();
            for (int i = 0; i < cases.size(); i++) {
        Map<String, Object> c = (Map<String, Object>) cases.get(i);
        List<Object> input = (List<Object>) c.get("input");
        String[][] tickets = toStringMatrix((List<Object>) input.get(0));
        String[] actual = new Solution().findItinerary(tickets);
        String[] expected = toStringArray((List<Object>) c.get("expected"));
        if (!Arrays.equals(actual, expected)) {
            Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
        }
                Common.reportProgress(i + 1, total);
    }

            Common.reportAC(total);
        }
    }
