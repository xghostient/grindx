import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * Shared judge utilities for Java judges.
 * Includes a minimal JSON parser for test case loading.
 */
public class Common {
    private static RandomAccessFile progressFile = null;

    // -----------------------------------------------------------------------
    // Minimal JSON parser — handles arrays, objects, strings, numbers, booleans, null
    // -----------------------------------------------------------------------

    public static Object parseJson(String json) {
        return new JsonParser(json.trim()).parseValue();
    }

    private static class JsonParser {
        private final String s;
        private int pos;

        JsonParser(String s) { this.s = s; this.pos = 0; }

        Object parseValue() {
            skipWhitespace();
            if (pos >= s.length()) return null;
            char c = s.charAt(pos);
            if (c == '"') return parseString();
            if (c == '{') return parseObject();
            if (c == '[') return parseArray();
            if (c == 't' || c == 'f') return parseBoolean();
            if (c == 'n') return parseNull();
            return parseNumber();
        }

        String parseString() {
            pos++; // skip opening quote
            StringBuilder sb = new StringBuilder();
            while (pos < s.length()) {
                char c = s.charAt(pos);
                if (c == '"') { pos++; return sb.toString(); }
                if (c == '\\') {
                    pos++;
                    char esc = s.charAt(pos);
                    switch (esc) {
                        case '"': case '\\': case '/': sb.append(esc); break;
                        case 'n': sb.append('\n'); break;
                        case 't': sb.append('\t'); break;
                        case 'r': sb.append('\r'); break;
                        default: sb.append(esc);
                    }
                } else {
                    sb.append(c);
                }
                pos++;
            }
            return sb.toString();
        }

        @SuppressWarnings("unchecked")
        Map<String, Object> parseObject() {
            pos++; // skip {
            Map<String, Object> map = new LinkedHashMap<>();
            skipWhitespace();
            if (pos < s.length() && s.charAt(pos) == '}') { pos++; return map; }
            while (pos < s.length()) {
                skipWhitespace();
                String key = parseString();
                skipWhitespace();
                pos++; // skip :
                Object value = parseValue();
                map.put(key, value);
                skipWhitespace();
                if (pos < s.length() && s.charAt(pos) == ',') pos++;
                else break;
            }
            skipWhitespace();
            if (pos < s.length() && s.charAt(pos) == '}') pos++;
            return map;
        }

        List<Object> parseArray() {
            pos++; // skip [
            List<Object> list = new ArrayList<>();
            skipWhitespace();
            if (pos < s.length() && s.charAt(pos) == ']') { pos++; return list; }
            while (pos < s.length()) {
                list.add(parseValue());
                skipWhitespace();
                if (pos < s.length() && s.charAt(pos) == ',') pos++;
                else break;
            }
            skipWhitespace();
            if (pos < s.length() && s.charAt(pos) == ']') pos++;
            return list;
        }

        Number parseNumber() {
            int start = pos;
            if (pos < s.length() && s.charAt(pos) == '-') pos++;
            while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            boolean isFloat = false;
            if (pos < s.length() && s.charAt(pos) == '.') {
                isFloat = true;
                pos++;
                while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            }
            if (pos < s.length() && (s.charAt(pos) == 'e' || s.charAt(pos) == 'E')) {
                isFloat = true;
                pos++;
                if (pos < s.length() && (s.charAt(pos) == '+' || s.charAt(pos) == '-')) pos++;
                while (pos < s.length() && Character.isDigit(s.charAt(pos))) pos++;
            }
            String num = s.substring(start, pos);
            if (isFloat) return Double.parseDouble(num);
            long val = Long.parseLong(num);
            if (val >= Integer.MIN_VALUE && val <= Integer.MAX_VALUE) return (int) val;
            return val;
        }

        Boolean parseBoolean() {
            if (s.startsWith("true", pos)) { pos += 4; return true; }
            pos += 5; return false;
        }

        Object parseNull() {
            pos += 4;
            return null;
        }

        void skipWhitespace() {
            while (pos < s.length() && Character.isWhitespace(s.charAt(pos))) pos++;
        }
    }

    // -----------------------------------------------------------------------
    // Test case loading
    // -----------------------------------------------------------------------

    @SuppressWarnings("unchecked")
    public static Map<String, Object> loadCases(String problemId) {
        try {
            // Resolve relative to the compiled class location (temp dir)
            String dir = System.getProperty("user.dir");
            String path = dir + File.separator + problemId + ".json";
            String content = new String(Files.readAllBytes(Paths.get(path)));
            return (Map<String, Object>) parseJson(content);
        } catch (IOException e) {
            System.err.println("Cannot read test cases: " + e.getMessage());
            System.exit(2);
            return null;
        }
    }

    // -----------------------------------------------------------------------
    // Data structures
    // -----------------------------------------------------------------------

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode() {}
        public ListNode(int val) { this.val = val; }
        public ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;
        public TreeNode() {}
        public TreeNode(int val) { this.val = val; }
        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val; this.left = left; this.right = right;
        }
    }

    public static class Node {
        public int val;
        public Node[] neighbors;
        public Node() { this.neighbors = new Node[0]; }
        public Node(int val) { this.val = val; this.neighbors = new Node[0]; }
        public Node(int val, Node[] neighbors) { this.val = val; this.neighbors = neighbors; }
    }

    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    public static int[] toIntArray(List<Object> list) {
        int[] arr = new int[list.size()];
        for (int i = 0; i < list.size(); i++) {
            arr[i] = ((Number) list.get(i)).intValue();
        }
        return arr;
    }

    @SuppressWarnings("unchecked")
    public static int[][] toIntMatrix(List<Object> rows) {
        int[][] matrix = new int[rows.size()][];
        for (int i = 0; i < rows.size(); i++) {
            matrix[i] = toIntArray((List<Object>) rows.get(i));
        }
        return matrix;
    }

    public static char[][] toCharMatrix(List<Object> rows) {
        char[][] matrix = new char[rows.size()][];
        for (int i = 0; i < rows.size(); i++) {
            matrix[i] = String.valueOf(rows.get(i)).toCharArray();
        }
        return matrix;
    }

    public static boolean[] toBooleanArray(List<Object> list) {
        boolean[] result = new boolean[list.size()];
        for (int i = 0; i < list.size(); i++) {
            result[i] = (Boolean) list.get(i);
        }
        return result;
    }

    @SuppressWarnings("unchecked")
    public static List<List<Integer>> normalizeNestedIntLists(List<Object> raw) {
        List<List<Integer>> result = new ArrayList<>();
        for (Object rowObj : raw) {
            List<Object> rowRaw = (List<Object>) rowObj;
            List<Integer> row = new ArrayList<>(rowRaw.size());
            for (Object value : rowRaw) {
                row.add(((Number) value).intValue());
            }
            Collections.sort(row);
            result.add(row);
        }
        result.sort(Comparator.comparing(Object::toString));
        return result;
    }

    public static int toInt(Object obj) {
        return ((Number) obj).intValue();
    }

    public static String truncate(String s, int maxLen) {
        if (s.length() <= maxLen) return s;
        return s.substring(0, maxLen - 3) + "...";
    }

    // -----------------------------------------------------------------------
    // Verdict reporting
    // -----------------------------------------------------------------------

    public static void reportProgress(int passed, int total) {
        String progressPath = System.getenv("GRINDX_PROGRESS_FILE");
        if (progressPath == null || progressPath.isEmpty()) {
            return;
        }
        try {
            if (progressFile == null) {
                progressFile = new RandomAccessFile(progressPath, "rw");
                progressFile.setLength(0);
            }
            String payload = passed + "," + total;
            progressFile.seek(0);
            progressFile.writeBytes(payload);
            progressFile.setLength(payload.length());
        } catch (IOException ignored) {
        }
    }

    public static void reportAC(int total) {
        System.out.println("{\"verdict\":\"AC\",\"passed\":" + total + ",\"total\":" + total + "}");
        System.exit(0);
    }

    @SuppressWarnings("unchecked")
    public static void reportWA(int caseIdx, Object input, Object expected, Object actual,
                                 int total, String category) {
        String inputStr = truncate(String.valueOf(input), 200);
        String expectedStr = truncate(String.valueOf(expected), 200);
        String actualStr = truncate(String.valueOf(actual), 200);
        System.out.println("{\"verdict\":\"WA\",\"failed_case\":" + caseIdx +
            ",\"input_preview\":\"" + escapeJson(inputStr) +
            "\",\"expected_preview\":\"" + escapeJson(expectedStr) +
            "\",\"actual_preview\":\"" + escapeJson(actualStr) +
            "\",\"passed\":" + caseIdx +
            ",\"total\":" + total +
            ",\"category\":\"" + escapeJson(category) + "\"}");
        System.exit(1);
    }

    private static String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t");
    }
}
