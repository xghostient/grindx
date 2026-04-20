        import java.util.*;

        class Judge {
        static int[][] cloneMatrix(int[][] matrix) {
    int[][] out = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) {
        out[i] = Arrays.copyOf(matrix[i], matrix[i].length);
    }
    return out;
}

@SuppressWarnings("unchecked")
static String[][] toStringMatrix(List<Object> raw) {
    String[][] out = new String[raw.size()][];
    for (int i = 0; i < raw.size(); i++) {
        List<Object> row = (List<Object>) raw.get(i);
        out[i] = new String[row.size()];
        for (int j = 0; j < row.size(); j++) {
            out[i][j] = String.valueOf(row.get(j));
        }
    }
    return out;
}

static List<List<String>> normalizeAccounts(String[][] accounts) {
    List<List<String>> result = new ArrayList<>();
    for (String[] account : accounts) {
        if (account.length == 0) continue;
        TreeSet<String> emails = new TreeSet<>();
        for (int i = 1; i < account.length; i++) emails.add(account[i]);
        List<String> row = new ArrayList<>();
        row.add(account[0]);
        row.addAll(emails);
        result.add(row);
    }
    result.sort(Comparator.comparing(Object::toString));
    return result;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("most-stones-removed-within-same-row");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[][] grid = Common.toIntMatrix((List<Object>) input.get(0));
    int actual = new Solution().removeStones(cloneMatrix(grid));
    int expected = Common.toInt(c.get("expected"));
    if (actual != expected) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
