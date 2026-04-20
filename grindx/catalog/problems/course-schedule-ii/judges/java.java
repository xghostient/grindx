        import java.util.*;

        class Judge {
        static int[][] cloneMatrix(int[][] matrix) {
    int[][] out = new int[matrix.length][];
    for (int i = 0; i < matrix.length; i++) {
        out[i] = Arrays.copyOf(matrix[i], matrix[i].length);
    }
    return out;
}

static boolean validTopologicalOrder(int[] order, int v, int[][] adj) {
    if (order == null || order.length != v) return false;
    int[] pos = new int[v];
    Arrays.fill(pos, -1);
    for (int i = 0; i < order.length; i++) {
        int node = order[i];
        if (node < 0 || node >= v || pos[node] != -1) return false;
        pos[node] = i;
    }
    for (int node = 0; node < v; node++) {
        if (pos[node] == -1) return false;
        for (int nei : adj[node]) {
            if (pos[node] >= pos[nei]) return false;
        }
    }
    return true;
}

static boolean validCourseOrder(int[] order, int numCourses, int[][] prerequisites) {
    if (order == null || order.length != numCourses) return false;
    int[] pos = new int[numCourses];
    Arrays.fill(pos, -1);
    for (int i = 0; i < order.length; i++) {
        int course = order[i];
        if (course < 0 || course >= numCourses || pos[course] != -1) return false;
        pos[course] = i;
    }
    for (int[] edge : prerequisites) {
        if (pos[edge[1]] >= pos[edge[0]]) return false;
    }
    return true;
}


            @SuppressWarnings("unchecked")
            public static void main(String[] args) {
                Map<String, Object> tc = Common.loadCases("course-schedule-ii");
                List<Object> cases = (List<Object>) tc.get("cases");
                int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
    Map<String, Object> c = (Map<String, Object>) cases.get(i);
    List<Object> input = (List<Object>) c.get("input");
    int numCourses = Common.toInt(input.get(0));
    int[][] prerequisites = Common.toIntMatrix((List<Object>) input.get(1));
    int[] actual = new Solution().findOrder(numCourses, cloneMatrix(prerequisites));
    int[] expected = Common.toIntArray((List<Object>) c.get("expected"));
    if (expected.length == 0) {
        if (actual == null || actual.length != 0) {
            Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
        }
    } else if (!validCourseOrder(actual, numCourses, prerequisites)) {
        Common.reportWA(i, input, Arrays.toString(expected), Arrays.toString(actual), total, (String) c.getOrDefault("category", ""));
    }
    Common.reportProgress(i + 1, total);
}

                Common.reportAC(total);
            }
        }
