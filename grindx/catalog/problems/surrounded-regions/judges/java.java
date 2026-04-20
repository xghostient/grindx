        import java.util.*;

        class Judge {
        static int[][] cloneMatrix(int[][] matrix) {
    int[][] out = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) {
        out[i] = Arrays.copyOf(matrix[i], matrix[i].length);
    }
    return out;
}

static char[][] stringRowsToGrid(List<Object> rows) {
    return Common.toCharMatrix(rows);
}

static List<String> gridToStringRows(char[][] board) {
    List<String> result = new ArrayList<>();
    for (char[] row : board) {
        result.add(new String(row));
    }
    return result;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("surrounded-regions");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    char[][] board = stringRowsToGrid((List<Object>) input.get(0));
    new Solution().solve(board);
    List<String> actual = gridToStringRows(board);
    List<String> expected = new ArrayList<>();
    for (Object row : (List<Object>) c.get("expected")) expected.add(String.valueOf(row));
    if (!actual.equals(expected)) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
