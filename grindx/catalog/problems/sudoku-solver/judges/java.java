        import java.util.*;

        class Judge {
        static int[] toIntArray(Object raw) {
    List<Object> values = (List<Object>) raw;
    int[] out = new int[values.size()];
    for (int i = 0; i < values.size(); i++) out[i] = Common.toInt(values.get(i));
    return out;
}

static List<Integer> toIntList(Object raw) {
    List<Object> values = (List<Object>) raw;
    List<Integer> out = new ArrayList<>();
    for (Object value : values) out.add(Common.toInt(value));
    return out;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("sudoku-solver");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    List<Object> rawBoard = (List<Object>) input.get(0);
    char[][] board = new char[9][9];
    for (int r = 0; r < 9; r++) {
        List<Object> row = (List<Object>) rawBoard.get(r);
        for (int cc = 0; cc < 9; cc++) board[r][cc] = String.valueOf(row.get(cc)).charAt(0);
    }
    new Solution().solveSudoku(board);
    List<Object> rawExpected = (List<Object>) c.get("expected");
    boolean match = true;
    for (int r = 0; r < 9 && match; r++) {
        List<Object> row = (List<Object>) rawExpected.get(r);
        for (int cc = 0; cc < 9 && match; cc++) {
            if (board[r][cc] != String.valueOf(row.get(cc)).charAt(0)) match = false;
        }
    }
    if (!match) {
        String[][] result = new String[9][9];
        for (int r = 0; r < 9; r++) for (int cc = 0; cc < 9; cc++) result[r][cc] = String.valueOf(board[r][cc]);
        Common.reportWA(i, input, c.get("expected"), Arrays.deepToString(result), total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
