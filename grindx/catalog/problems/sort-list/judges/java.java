import java.util.*;

class Judge {
    static List<Map<String, Object>> generateLargeCases() {
        List<Map<String, Object>> out = new ArrayList<>();

        int[] descending = new int[50000];
        int[] descendingExpected = new int[50000];
        for (int i = 0; i < 50000; i++) {
            descending[i] = 50000 - i;
            descendingExpected[i] = i + 1;
        }

        int[] mixed = new int[50000];
        for (int i = 0; i < mixed.length; i++) {
            mixed[i] = ((i * 8191) % 200001) - 100000;
        }
        int[] mixedExpected = Arrays.copyOf(mixed, mixed.length);
        Arrays.sort(mixedExpected);

        int[] duplicates = new int[50000];
        for (int i = 0; i < duplicates.length; i++) {
            duplicates[i] = ((i * 37) % 31) - 15;
        }
        int[] duplicatesExpected = Arrays.copyOf(duplicates, duplicates.length);
        Arrays.sort(duplicatesExpected);

        out.add(makeCase(descending, descendingExpected));
        out.add(makeCase(mixed, mixedExpected));
        out.add(makeCase(duplicates, duplicatesExpected));
        return out;
    }

    static Map<String, Object> makeCase(int[] input, int[] expected) {
        Map<String, Object> c = new HashMap<>();
        List<Object> wrappedInput = new ArrayList<>();
        List<Object> inputList = new ArrayList<>(input.length);
        for (int value : input) inputList.add(value);
        wrappedInput.add(inputList);
        c.put("input", wrappedInput);
        List<Object> expectedList = new ArrayList<>(expected.length);
        for (int value : expected) expectedList.add(value);
        c.put("expected", expectedList);
        c.put("category", "stress");
        return c;
    }

    static ListNode listToLinkedList(int[] arr) {
        if (arr.length == 0) return null;
        ListNode head = new ListNode(arr[0]);
        ListNode cur = head;
        for (int i = 1; i < arr.length; i++) {
            cur.next = new ListNode(arr[i]);
            cur = cur.next;
        }
        return head;
    }

    static List<Integer> linkedListToList(ListNode head) {
        List<Integer> out = new ArrayList<>();
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) {
                out.add(Integer.MIN_VALUE);
                return out;
            }
            out.add(head.val);
            head = head.next;
        }
        return out;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) {
        Map<String, Object> tc = Common.loadCases("sort-list");
        List<Object> cases = new ArrayList<>((List<Object>) tc.get("cases"));
        cases.addAll(generateLargeCases());
        int total = cases.size();
        for (int i = 0; i < cases.size(); i++) {
            Map<String, Object> c = (Map<String, Object>) cases.get(i);
            List<Object> input = (List<Object>) c.get("input");
            int[] arr = Common.toIntArray((List<Object>) input.get(0));
            List<Integer> actual = linkedListToList(new Solution().sortList(listToLinkedList(arr)));
            int[] expectedRaw = Common.toIntArray((List<Object>) c.get("expected"));
            List<Integer> expected = new ArrayList<>();
            for (int value : expectedRaw) expected.add(value);
            if (!actual.equals(expected)) {
                Common.reportWA(i, input, expected.toString(), actual.toString(), total, (String) c.getOrDefault("category", ""));
            }
            Common.reportProgress(i + 1, total);
        }
        Common.reportAC(total);
    }
}
