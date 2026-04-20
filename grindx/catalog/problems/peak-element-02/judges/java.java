        import java.util.*;

        class Judge {
        static int[] toIntArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    int[] out = new int[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = Common.toInt(values.get(i));
    return out;
}

static int[][] toIntMatrix(Object raw) {
    List<Object> rows = (List<Object>) raw;
    int[][] out = new int[rows.size()][];
    for (int i = 0; i < rows.size(); i++) out[i] = toIntArray(rows.get(i));
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("peak-element-02");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
                for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[][] mat = toIntMatrix(input.get(0));
            int[] result = new Solution().findPeakGrid(mat);
            int rows = mat.length, cols = mat[0].length;
            boolean valid = result != null && result.length == 2;
            int r = 0, cc = 0;
            if (valid) {
                r = result[0];
                cc = result[1];
                valid = r >= 0 && r < rows && cc >= 0 && cc < cols;
            }
            if (valid) {
                int val = mat[r][cc];
                if (r > 0 && mat[r - 1][cc] >= val) valid = false;
                if (r < rows - 1 && mat[r + 1][cc] >= val) valid = false;
                if (cc > 0 && mat[r][cc - 1] >= val) valid = false;
                if (cc < cols - 1 && mat[r][cc + 1] >= val) valid = false;
            }
            if (!valid) Common.reportWA(i, input, "valid 2D peak", result == null ? "null" : Arrays.toString(result), total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
                Common.reportAC(total);
            }
        }
