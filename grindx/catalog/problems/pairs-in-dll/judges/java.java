import java.util.*;

class Judge {
    static DLLNode listToDLL(int[] arr) {
        if (arr.length == 0) return null;
        DLLNode head = new DLLNode(arr[0]);
        DLLNode cur = head;
        for (int i = 1; i < arr.length; i++) {
            DLLNode node = new DLLNode(arr[i]);
            node.prev = cur;
            cur.next = node;
            cur = node;
        }
        return head;
    }

    static List<List<Integer>> normalizePairs(int[][] result) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] pair : result) out.add(Arrays.asList(pair[0], pair[1]));
        out.sort(Comparator.comparing(Object::toString));
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("pairs-in-dll");
        List<Object> cases = (List<Object>) tc.get("cases");
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            List<List<Integer>> actual = normalizePairs(new Solution().findPairs(listToDLL(Common.toIntArray((List<Object>) input.get(0))), Common.toInt(input.get(1))));
            List<List<Integer>> expected = Common.normalizeNestedIntLists((List<Object>) c.get("expected"));
            if (!actual.equals(expected)) {
                Common.reportWA(i, input, expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
