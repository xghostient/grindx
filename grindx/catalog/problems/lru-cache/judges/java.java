import java.util.*;

/**
 * Judge for LRU Cache — design class pattern.
 */
class Judge {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("lru-cache");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size() + 1;

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            String failMsg = runCase(c);
            if (failMsg != null) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, "LRU operations", "correct outputs",
                    failMsg, total, category);
            }
            Common.reportProgress(i + 1, total);
        }

        runLargeCase(total, cases.size());

        Common.reportAC(total);
    }

    @SuppressWarnings("unchecked")
    private static String runCase(Map<String, Object> c) {
        List<Object> input = (List<Object>) c.get("input");
        int capacity = Common.toInt(input.get(0));
        List<Object> operations = (List<Object>) c.get("operations");
        List<Object> opInputs = (List<Object>) c.get("op_inputs");
        List<Object> expected = (List<Object>) c.get("expected");

        LRUCache cache = new LRUCache(capacity);

        for (int j = 0; j < operations.size(); j++) {
            String op = (String) operations.get(j);
            List<Object> opArgs = (List<Object>) opInputs.get(j);

            if (op.equals("put")) {
                int key = Common.toInt(opArgs.get(0));
                int value = Common.toInt(opArgs.get(1));
                cache.Put(key, value);
            } else if (op.equals("get")) {
                int key = Common.toInt(opArgs.get(0));
                int result = cache.Get(key);
                if (expected.get(j) != null) {
                    int exp = Common.toInt(expected.get(j));
                    if (result != exp) {
                        return "op " + j + " get(" + key + "): expected " + exp + ", got " + result;
                    }
                }
            }
        }
        return null;
    }

    private static void runLargeCase(int total, int caseIndex) {
        int capacity = 3000;
        int totalOps = 200000;
        LRUCache cache = new LRUCache(capacity);

        // Reference implementation for expected values
        LinkedHashMap<Integer, Integer> ref = new LinkedHashMap<Integer, Integer>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > capacity;
            }
        };

        for (int key = 0; key < capacity; key++) {
            int value = (key * 97) % 100001;
            cache.Put(key, value);
            ref.put(key, value);
        }

        for (int step = 0; step < totalOps - capacity; step++) {
            int key = (step * 1879) % capacity;
            if ((step & 1) == 0) {
                int actual = cache.Get(key);
                Integer expected = ref.get(key);
                int expectedVal = expected != null ? expected : -1;
                if (actual != expectedVal) {
                    Common.reportWA(
                        caseIndex,
                        "stress op " + step + ": get(" + key + ")",
                        Integer.toString(expectedVal),
                        Integer.toString(actual),
                        total,
                        "stress"
                    );
                }
            } else {
                int value = ((step * 7919) + key) % 100001;
                cache.Put(key, value);
                ref.put(key, value);
            }
        }
    }
}
