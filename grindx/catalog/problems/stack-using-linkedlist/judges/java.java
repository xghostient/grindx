            import java.util.*;

            class Judge {
            static int[] toIntArray(List<Object> raw) {
    int[] out = new int[raw.size()];
    for (int i = 0; i < raw.size(); i++) out[i] = ((Number) raw.get(i)).intValue();
    return out;
}

static List<String> toStringList(List<Object> raw) {
    List<String> out = new ArrayList<>();
    for (Object value : raw) out.add(String.valueOf(value));
    return out;
}

static List<String> sortedStrings(List<String> raw) {
    List<String> out = new ArrayList<>(raw);
    Collections.sort(out);
    return out;
}

@SuppressWarnings("unchecked")
static List<String> normalizeStringResult(Object raw) {
    if (raw instanceof String[]) {
        return sortedStrings(Arrays.asList((String[]) raw));
    }
    if (raw instanceof List<?>) {
        List<String> out = new ArrayList<>();
        for (Object value : (List<Object>) raw) out.add(String.valueOf(value));
        return sortedStrings(out);
    }
    return new ArrayList<>();
}


                @SuppressWarnings("unchecked")
                public static void main(String[] args) {
                    Map<String, Object> tc = Common.loadCases("stack-using-linkedlist");
                    List<Object> cases = (List<Object>) tc.get("cases");
                    int total = cases.size();
                    for (int i = 0; i < cases.size(); i++) {
                        Map<String, Object> c = (Map<String, Object>) cases.get(i);
                        Stack obj = new Stack();
                        List<Object> ops = (List<Object>) c.get("operations");
                        List<Object> opInputs = (List<Object>) c.get("op_inputs");
                        List<Object> expected = (List<Object>) c.get("expected");
                        for (int j = 0; j < ops.size(); j++) {
                            String op = String.valueOf(ops.get(j));
                            List<Object> argsIn = (List<Object>) opInputs.get(j);
                            Object want = expected.get(j);
                            Object actual = null;
                                        if (op.equals("push")) {
                                            obj.Push(Common.toInt(argsIn.get(0))); actual = null;
                                        }
                                        if (op.equals("pop")) {
                                            actual = obj.Pop();
                                        }
                                        if (op.equals("top")) {
                                            actual = obj.Top();
                                        }
                                        if (op.equals("isEmpty")) {
                                            actual = obj.IsEmpty();
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
