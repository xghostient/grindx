import java.util.*;

class Judge {
    private static final class LargeCase {
        final int n;
        final int[][] unions;
        final int[][] queries;
        final boolean[] expected;

        LargeCase(int n, int[][] unions, int[][] queries, boolean[] expected) {
            this.n = n;
            this.unions = unions;
            this.queries = queries;
            this.expected = expected;
        }
    }

    private static List<LargeCase> generateLargeCases() {
        ArrayList<LargeCase> cases = new ArrayList<>(4);
        for (int variant = 0; variant < 4; variant++) {
            int n = 100000;
            int[][] unions = new int[n - 1][2];
            for (int i = 0; i < n - 1; i++) {
                unions[i][0] = i;
                unions[i][1] = i + 1;
            }
            int[][] queries = new int[100000][2];
            if (variant == 0) {
                for (int i = 0; i < 100000; i++) {
                    queries[i][0] = 0;
                    queries[i][1] = n - 1;
                }
            } else if (variant == 1) {
                for (int i = 0; i < 100000; i++) {
                    queries[i][0] = 0;
                    queries[i][1] = n - 1 - i;
                }
            } else if (variant == 2) {
                for (int i = 0; i < 100000; i++) {
                    queries[i][0] = i;
                    queries[i][1] = n - 1;
                }
            } else {
                for (int i = 0; i < 50000; i++) {
                    queries[2 * i][0] = 0;
                    queries[2 * i][1] = n / 2;
                    queries[2 * i + 1][0] = n / 3;
                    queries[2 * i + 1][1] = n - 1;
                }
            }
            boolean[] expected = new boolean[queries.length];
            Arrays.fill(expected, true);
            cases.add(new LargeCase(n, unions, queries, expected));
        }
        return cases;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("union-find");
        List<Object> cases = (List<Object>) tc.get("cases");
        List<LargeCase> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int n = Common.toInt(input.get(0));
            int[][] unions = Common.toIntMatrix((List<Object>) input.get(1));
            int[][] queries = Common.toIntMatrix((List<Object>) input.get(2));
            boolean[] expected = Common.toBooleanArray((List<Object>) c.get("expected"));
            UnionFind uf = new UnionFind(n);
            for (int[] pair : unions) {
                uf.Union(pair[0], pair[1]);
            }
            boolean[] actual = new boolean[queries.length];
            for (int q = 0; q < queries.length; q++) {
                actual[q] = uf.Connected(queries[q][0], queries[q][1]);
            }
            if (!Arrays.equals(actual, expected)) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        for (int li = 0; li < largeCases.size(); li++) {
            LargeCase c = largeCases.get(li);
            UnionFind uf = new UnionFind(c.n);
            for (int[] pair : c.unions) {
                uf.Union(pair[0], pair[1]);
            }
            boolean[] actual = new boolean[c.queries.length];
            for (int q = 0; q < c.queries.length; q++) {
                actual[q] = uf.Connected(c.queries[q][0], c.queries[q][1]);
            }
            if (!Arrays.equals(actual, c.expected)) {
                Common.reportWA(cases.size() + li, "large input", Arrays.toString(c.expected), Arrays.toString(actual), total, "tle");
            }
        }

        Common.reportAC(total);
    }
}
