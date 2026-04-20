import java.util.*;

class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("implement-trie-prefix-tree");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> cInput = (List<Object>) c.getOrDefault("input", List.of());
            Trie obj = new Trie();
            List<Object> ops = (List<Object>) c.get("operations");
            List<Object> opInputs = (List<Object>) c.get("op_inputs");
            List<Object> expected = (List<Object>) c.get("expected");
            for (int j = 0; j < ops.size(); j++) {
                String op = String.valueOf(ops.get(j));
                List<Object> argsIn = (List<Object>) opInputs.get(j);
                Object want = expected.get(j);
                Object actual = null;
                            if (op.equals("insert")) {
                                obj.Insert(String.valueOf(argsIn.get(0))); actual = null;
                            }
                            if (op.equals("search")) {
                                actual = obj.Search(String.valueOf(argsIn.get(0)));
                            }
                            if (op.equals("startsWith")) {
                                actual = obj.StartsWith(String.valueOf(argsIn.get(0)));
                            }
                if (!Objects.equals(actual, want)) {
                    Common.reportWA(i, Arrays.asList(op, argsIn), want, actual, total, (String) c.getOrDefault("category", ""));
                }
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
