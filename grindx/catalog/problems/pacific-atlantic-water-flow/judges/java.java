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

static List<List<Integer>> normalizePairs(List<List<Integer>> raw) {
    List<List<Integer>> result = new ArrayList<>();
    for (List<Integer> row : raw) {
        result.add(new ArrayList<>(row));
    }
    result.sort((a, b) -> {
        if (!Objects.equals(a.get(0), b.get(0))) return Integer.compare(a.get(0), b.get(0));
        return Integer.compare(a.get(1), b.get(1));
    });
    return result;
}

static List<List<Integer>> normalizePairsMatrix(int[][] raw) {
    List<List<Integer>> result = new ArrayList<>();
    for (int[] row : raw) {
        result.add(Arrays.asList(row[0], row[1]));
    }
    return normalizePairs(result);
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("pacific-atlantic-water-flow");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int[][] heights = Common.toIntMatrix((List<Object>) input.get(0));
    int[][] rawActual = new Solution().pacificAtlantic(cloneMatrix(heights));
    List<List<Integer>> actual = normalizePairsMatrix(rawActual);
    List<List<Integer>> expected = new ArrayList<>();
    for (Object rowObj : (List<Object>) c.get("expected")) {
        List<Object> rowRaw = (List<Object>) rowObj;
        expected.add(Arrays.asList(Common.toInt(rowRaw.get(0)), Common.toInt(rowRaw.get(1))));
    }
    expected = normalizePairs(expected);
    if (!actual.equals(expected)) {
        Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
