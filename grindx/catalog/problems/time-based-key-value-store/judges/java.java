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
                    Map<String, Object> tc = Common.loadCases("time-based-key-value-store");
                    List<Object> cases = (List<Object>) tc.get("cases");
                    int total = cases.size();
                    for (int i = 0; i < cases.size(); i++) {
                        Map<String, Object> c = (Map<String, Object>) cases.get(i);
                        TimeMap obj = new TimeMap();
                        List<Object> ops = (List<Object>) c.get("operations");
                        List<Object> opInputs = (List<Object>) c.get("op_inputs");
                        List<Object> expected = (List<Object>) c.get("expected");
                        for (int j = 0; j < ops.size(); j++) {
                            String op = String.valueOf(ops.get(j));
                            List<Object> argsIn = (List<Object>) opInputs.get(j);
                            Object want = expected.get(j);
                            Object actual = null;
                            if (op.equals("TimeMap")) {
                                actual = null;
                            } else if (op.equals("set")) {
                                obj.Set(String.valueOf(argsIn.get(0)), String.valueOf(argsIn.get(1)), Common.toInt(argsIn.get(2)));
                                actual = null;
                            } else if (op.equals("get")) {
                                actual = obj.Get(String.valueOf(argsIn.get(0)), Common.toInt(argsIn.get(1)));
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
