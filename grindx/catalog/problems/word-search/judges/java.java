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
                Map<String, Object> tc = Common.loadCases("word-search");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    List<Object> rawBoard = (List<Object>) input.get(0);
    char[][] board = new char[rawBoard.size()][];
    for (int r = 0; r < rawBoard.size(); r++) {
        List<Object> row = (List<Object>) rawBoard.get(r);
        board[r] = new char[row.size()];
        for (int cc = 0; cc < row.size(); cc++) board[r][cc] = String.valueOf(row.get(cc)).charAt(0);
    }
    String word = String.valueOf(input.get(1));
    boolean actual = new Solution().exist(board, word);
    boolean expected = (Boolean) c.get("expected");
    if (actual != expected) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
