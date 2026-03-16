import java.util.*;

/**
 * Judge for LRU Cache — design class pattern.
 */
class Judge {

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("lru-cache");
        List<Object> cases = (List<Object>) tc.get("cases");

        // Generate large case for TLE detection
        List<Map<String, Object>> largeCases = generateLargeCases();
        int total = cases.size() + largeCases.size();

        // Basic cases
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            String failMsg = runCase(c);
            if (failMsg != null) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(i, "LRU operations", "correct outputs",
                    failMsg, total, category);
            }
        }

        // Large cases
        for (int li = 0; li < largeCases.size(); li++) {
            int idx = cases.size() + li;
            Map<String, Object> c = largeCases.get(li);
            String failMsg = runCase(c);
            if (failMsg != null) {
                String category = c.containsKey("category") ? (String) c.get("category") : "";
                Common.reportWA(idx, "large LRU operations", "correct outputs",
                    failMsg, total, category);
            }
        }

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

    @SuppressWarnings("unchecked")
    private static List<Map<String, Object>> generateLargeCases() {
        List<Map<String, Object>> cases = new ArrayList<>();
        Random rng = new Random(42);
        int capacity = 1000;
        int numOps = 100000;

        List<Object> operations = new ArrayList<>();
        List<Object> opInputs = new ArrayList<>();
        List<Object> expected = new ArrayList<>();

        // Reference implementation for expected values
        LinkedHashMap<Integer, Integer> ref = new LinkedHashMap<Integer, Integer>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > capacity;
            }
        };

        for (int j = 0; j < numOps; j++) {
            if (rng.nextInt(3) < 2) {
                // put operation (2/3 of the time)
                int key = rng.nextInt(5000);
                int value = rng.nextInt(100000);
                operations.add("put");
                List<Object> opArgs = new ArrayList<>();
                opArgs.add(key);
                opArgs.add(value);
                opInputs.add(opArgs);
                expected.add(null);
                ref.put(key, value);
            } else {
                // get operation (1/3 of the time)
                int key = rng.nextInt(5000);
                operations.add("get");
                List<Object> opArgs = new ArrayList<>();
                opArgs.add(key);
                opInputs.add(opArgs);
                Integer val = ref.get(key);
                expected.add(val != null ? val : -1);
            }
        }

        Map<String, Object> largeCase = new LinkedHashMap<>();
        List<Object> input = new ArrayList<>();
        input.add(capacity);
        largeCase.put("input", input);
        largeCase.put("operations", operations);
        largeCase.put("op_inputs", opInputs);
        largeCase.put("expected", expected);
        largeCase.put("category", "tle");
        cases.add(largeCase);
        return cases;
    }
}
