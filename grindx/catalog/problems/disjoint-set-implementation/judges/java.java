import java.util.*;

class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("disjoint-set-implementation");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            int n = Common.toInt(((List<Object>) c.get("input")).get(0));
            DSU dsu = new DSU(n);
            List<Object> ops = (List<Object>) c.get("operations");
            List<Object> opInputs = (List<Object>) c.get("op_inputs");
            List<Object> expected = (List<Object>) c.get("expected");
            for (int j = 0; j < ops.size(); j++) {
                String op = String.valueOf(ops.get(j));
                List<Object> argsIn = (List<Object>) opInputs.get(j);
                int a = Common.toInt(argsIn.get(0));
                int b = Common.toInt(argsIn.get(1));
                boolean actual = op.equals("union") ? dsu.Union(a, b) : dsu.Find(a) == dsu.Find(b);
                boolean want = (Boolean) expected.get(j);
                if (actual != want) {
                    Common.reportWA(i, Arrays.asList(op, a, b), want, actual, total, (String) c.getOrDefault("category", ""));
                }
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
