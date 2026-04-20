        import java.util.*;

        class Judge {
        static int[][] cloneMatrix(int[][] matrix) {
    int[][] out = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) out[i] = Arrays.copyOf(matrix[i], matrix[i].length);
    return out;
}
@SuppressWarnings("unchecked")
static int[][][] toIntTensor3(List<Object> raw) {
    int[][][] out = new int[raw.size()][][];
    for (int i = 0; i < raw.size(); i++) {
        List<Object> row = (List<Object>) raw.get(i);
        out[i] = new int[row.size()][2];
        for (int j = 0; j < row.size(); j++) {
            List<Object> edge = (List<Object>) row.get(j);
            out[i][j][0] = Common.toInt(edge.get(0));
            out[i][j][1] = Common.toInt(edge.get(1));
        }
    }
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("min-cost-to-connect-all-points");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) { Map<String, Object> c = (Map<String, Object>) cases.get(i); List<Object> in = (List<Object>) c.get("input"); int[][] grid = Common.toIntMatrix((List<Object>) in.get(0)); int actual = new Solution().minCostConnectPoints(cloneMatrix(grid)); int expected = Common.toInt(c.get("expected")); if (actual != expected) Common.reportWA(i, in, expected, actual, total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
