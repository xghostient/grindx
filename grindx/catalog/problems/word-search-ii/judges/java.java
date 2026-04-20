import java.util.*;

class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("word-search-ii");
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
                for (int ci = 0; ci < row.size(); ci++) board[r][ci] = String.valueOf(row.get(ci)).charAt(0);
            }
            List<Object> rawWords = (List<Object>) input.get(1);
            String[] words = new String[rawWords.size()];
            for (int k = 0; k < rawWords.size(); k++) words[k] = String.valueOf(rawWords.get(k));
            String[] result = new Solution().findWords(board, words);
            List<String> actual = new ArrayList<>(Arrays.asList(result));
            Collections.sort(actual);
            List<String> expected = new ArrayList<>();
            for (Object o : (List<Object>) c.get("expected")) expected.add(String.valueOf(o));
            Collections.sort(expected);
            if (!actual.equals(expected)) Common.reportWA(i, input, expected, actual, total, (String) c.getOrDefault("category", ""));
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
