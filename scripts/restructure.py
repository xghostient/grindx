"""One-time migration: restructure into problems/ + thin sheets."""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent
SHEETS_DIR = BASE / "sheets"
PROBLEMS_DIR = BASE / "problems"
ENRICHED_DIR = BASE / "enriched"

# ─── Striver abbreviated → canonical LeetCode slug ───

STRIVER_TO_CANONICAL = {
    "2-sum": "two-sum",
    "3-sum": "3sum",
    "3-sum-closest": "3sum-closest",
    "4-sum": "4sum",
    "best-time-to-buy-sell-stock": "best-time-to-buy-and-sell-stock",
    "max-sum-subarray": "maximum-subarray",
    "print-max-sum-subarr": "maximum-subarray",
    "max-product-subarr": "maximum-product-subarray",
    "longest-consecutive-subseq": "longest-consecutive-sequence",
    "set-matrix-zero": "set-matrix-zeroes",
    "merge-sorted-arr": "merge-sorted-array",
    "move-zeros-to-end": "move-zeroes",
    "remove-duplicates-sorted-arr": "remove-duplicates-from-sorted-array",
    "sort-0s-1s-2s": "sort-colors",
    "subarr-sum-eq-k": "subarray-sum-equals-k",
    "pascal-triang": "pascals-triangle",
    "rotate-array-d-places": "rotate-array",
    "2d-matrix-binary-search": "search-a-2d-matrix",
    "min-in-rotated-array": "find-minimum-in-rotated-sorted-array",
    "search-rot-sorted-1": "search-in-rotated-sorted-array",
    "search-rot-sorted-2": "search-in-rotated-sorted-array-ii",
    "median-of-two-sorted-arr": "median-of-two-sorted-arrays",
    "ship-packages": "capacity-to-ship-packages-within-d-days",
    "split-largest": "split-array-largest-sum",
    "sqrt": "sqrtx",
    "first-last-index": "find-first-and-last-position-of-element-in-sorted-array",
    "longest-palindromic-substr": "longest-palindromic-substring",
    "valid-anagrams": "valid-anagram",
    "rev-words": "reverse-words-in-a-string",
    "roman-to-int": "roman-to-integer",
    "implement-atoi": "string-to-integer-atoi",
    "find-index-of-first-occurence": "find-the-index-of-the-first-occurrence-in-a-string",
    "sort-chars-by-freq": "sort-characters-by-frequency",
    "min-add-to-make-parantheses": "minimum-add-to-make-parentheses-valid",
    "remove-outer-paranth": "remove-outermost-parentheses",
    "count-say": "count-and-say",
    "reverse-ll": "reverse-linked-list",
    "detect-cycle": "linked-list-cycle",
    "detect-cycle-ii": "linked-list-cycle-ii",
    "remove-nth-node": "remove-nth-node-from-end-of-list",
    "intersection-of-ll": "intersection-of-two-linked-lists",
    "reverse-nodes-in-group-of-k": "reverse-nodes-in-k-group",
    "clone-list": "copy-list-with-random-pointer",
    "merge-k-linkedlists": "merge-k-sorted-lists",
    "flatten-ll": "flatten-a-multilevel-doubly-linked-list",
    "odd-even-grouping": "odd-even-linked-list",
    "tortoise-hair-method": "linked-list-cycle",
    "palindrome": "palindrome-linked-list",
    "combination-sum-1": "combination-sum",
    "combination-sum-2": "combination-sum-ii",
    "combination-sum-3": "combination-sum-iii",
    "generate-parantheses": "generate-parentheses",
    "n-queen": "n-queens",
    "phone-number": "letter-combinations-of-a-phone-number",
    "subset-sum-1": "subsets",
    "subset-sum-2": "subsets-ii",
    "count-set-bits": "number-of-1-bits",
    "divide-two-int": "divide-two-integers",
    "reverse-number": "reverse-integer",
    "valid-parantheses": "valid-parentheses",
    "queue-using-stack": "implement-queue-using-stacks",
    "trapping-rainwater": "trapping-rain-water",
    "stock-span": "online-stock-span",
    "next-greater-element-2": "next-greater-element-ii",
    "min-window-substring": "minimum-window-substring",
    "longest-rep-chars-replace": "longest-repeating-character-replacement",
    "longest-substr-rep-chars": "longest-substring-without-repeating-characters",
    "max-consec-ones": "max-consecutive-ones-iii",
    "max-points-obtained-from-cards": "maximum-points-you-can-obtain-from-cards",
    "k-most-frequent": "top-k-frequent-elements",
    "kth-largest": "kth-largest-element-in-an-array",
    "kth-largest-in-stream": "kth-largest-element-in-a-stream",
    "median-data-stream": "find-median-from-data-stream",
    "merge-k-sorted-arr": "merge-k-sorted-lists",
    "sliding-window-max": "sliding-window-maximum",
    "jump-game-01": "jump-game",
    "jump-game-02": "jump-game-ii",
    "gas-stations": "gas-station",
    "valid-parantheses-01": "valid-parenthesis-string",
    "valid-parantheses-02": "minimum-add-to-make-parentheses-valid",
    "max-depth-of-binary-tree": "maximum-depth-of-binary-tree",
    "max-path-sum": "binary-tree-maximum-path-sum",
    "bfs-traversals": "binary-tree-level-order-traversal",
    "kth-smallest-element-in-bst": "kth-smallest-element-in-a-bst",
    "validate-bst": "validate-binary-search-tree",
    "construct-binary-tree-from-pre-in-traversal": "construct-binary-tree-from-preorder-and-inorder-traversal",
    "serialise-deserialise": "serialize-and-deserialize-binary-tree",
    "convert-sorted-arr-to-bst": "convert-sorted-array-to-binary-search-tree",
    "count-good-nodes": "count-good-nodes-in-binary-tree",
    "search-in-bst": "search-in-a-binary-search-tree",
    "rotten-oranges": "rotting-oranges",
    "number-provinces": "number-of-provinces",
    "account-merge": "accounts-merge",
    "aliens-dictionary": "alien-dictionary",
    "course-schedule-1": "course-schedule",
    "course-schedule-2": "course-schedule-ii",
    "cheapest-flight-k-stops": "cheapest-flights-within-k-stops",
    "network-delay": "network-delay-time",
    "word-ladder-1": "word-ladder",
    "word-ladder-2": "word-ladder-ii",
    "house-robber-1": "house-robber",
    "house-robber-2": "house-robber-ii",
    "unique-paths-1": "unique-paths",
    "unique-paths-2": "unique-paths-ii",
    "burst-balloon-02": "burst-balloons",
    "longest-common-subseq": "longest-common-subsequence",
    "distinct-subseq": "distinct-subsequences",
    "longest-palindromic-subseq": "longest-palindromic-subsequence",
    "subseq-02-partition-equal-subset-sum": "partition-equal-subset-sum",
    "subseq-06-coin-change": "coin-change",
    "subseq-07-target-sum": "target-sum",
    "subseq-08-coin-change2": "coin-change-ii",
    "stocks-1": "best-time-to-buy-and-sell-stock",
    "stocks-2": "best-time-to-buy-and-sell-stock-ii",
    "stocks-3": "best-time-to-buy-and-sell-stock-iii",
    "stocks-4": "best-time-to-buy-and-sell-stock-iv",
    "stocks-5": "best-time-to-buy-and-sell-stock-with-cooldown",
    "stocks-6": "best-time-to-buy-and-sell-stock-with-transaction-fee",
    "implement-trie": "implement-trie-prefix-tree",
    "design-add-search-data-structure": "design-add-and-search-words-data-structure",
    "word-search-2": "word-search-ii",
}

# ─── Known LeetCode difficulties ───

KNOWN_DIFFICULTY = {
    "two-sum": "Easy", "3sum": "Medium", "3sum-closest": "Medium", "4sum": "Medium",
    "best-time-to-buy-and-sell-stock": "Easy", "maximum-subarray": "Medium",
    "maximum-product-subarray": "Medium", "longest-consecutive-sequence": "Medium",
    "set-matrix-zeroes": "Medium", "merge-sorted-array": "Easy", "move-zeroes": "Easy",
    "remove-duplicates-from-sorted-array": "Easy", "sort-colors": "Medium",
    "subarray-sum-equals-k": "Medium", "pascals-triangle": "Easy", "rotate-array": "Medium",
    "contains-duplicate": "Easy", "product-of-array-except-self": "Medium",
    "container-with-most-water": "Medium", "majority-element": "Easy",
    "find-minimum-in-rotated-sorted-array": "Medium",
    "search-in-rotated-sorted-array": "Medium", "search-in-rotated-sorted-array-ii": "Medium",
    "median-of-two-sorted-arrays": "Hard", "search-a-2d-matrix": "Medium",
    "koko-eating-bananas": "Medium", "capacity-to-ship-packages-within-d-days": "Medium",
    "split-array-largest-sum": "Hard", "sqrtx": "Easy",
    "find-first-and-last-position-of-element-in-sorted-array": "Medium",
    "binary-search": "Easy", "search-insert-position": "Easy",
    "longest-palindromic-substring": "Medium", "valid-anagram": "Easy",
    "reverse-words-in-a-string": "Medium", "roman-to-integer": "Easy",
    "string-to-integer-atoi": "Medium", "sort-characters-by-frequency": "Medium",
    "longest-common-prefix": "Easy", "count-and-say": "Medium",
    "remove-outermost-parentheses": "Easy",
    "find-the-index-of-the-first-occurrence-in-a-string": "Easy",
    "minimum-add-to-make-parentheses-valid": "Medium",
    "reverse-linked-list": "Easy", "linked-list-cycle": "Easy",
    "linked-list-cycle-ii": "Medium", "remove-nth-node-from-end-of-list": "Medium",
    "intersection-of-two-linked-lists": "Easy", "reverse-nodes-in-k-group": "Hard",
    "copy-list-with-random-pointer": "Medium", "merge-k-sorted-lists": "Hard",
    "flatten-a-multilevel-doubly-linked-list": "Medium", "odd-even-linked-list": "Medium",
    "add-two-numbers": "Medium", "sort-list": "Medium", "palindrome-linked-list": "Easy",
    "merge-two-sorted-lists": "Easy", "reorder-list": "Medium",
    "middle-of-the-linked-list": "Easy", "lru-cache": "Medium",
    "find-the-duplicate-number": "Medium", "rotate-list": "Medium",
    "combination-sum": "Medium", "combination-sum-ii": "Medium",
    "combination-sum-iii": "Medium", "combination-sum-iv": "Medium",
    "generate-parentheses": "Medium", "n-queens": "Hard",
    "letter-combinations-of-a-phone-number": "Medium", "subsets": "Medium",
    "subsets-ii": "Medium", "permutations": "Medium", "word-search": "Medium",
    "palindrome-partitioning": "Medium", "sudoku-solver": "Hard",
    "number-of-1-bits": "Easy", "divide-two-integers": "Medium",
    "reverse-integer": "Medium", "power-of-two": "Easy", "counting-bits": "Easy",
    "missing-number": "Easy", "reverse-bits": "Easy", "single-number": "Easy",
    "sum-of-two-integers": "Medium",
    "valid-parentheses": "Easy", "implement-queue-using-stacks": "Easy",
    "trapping-rain-water": "Hard", "online-stock-span": "Medium",
    "next-greater-element-ii": "Medium", "remove-k-digits": "Medium",
    "largest-rectangle-in-histogram": "Hard", "min-stack": "Medium",
    "sum-of-subarray-minimums": "Medium", "sum-of-subarray-ranges": "Medium",
    "daily-temperatures": "Medium", "car-fleet": "Medium",
    "evaluate-reverse-polish-notation": "Medium",
    "minimum-window-substring": "Hard",
    "longest-repeating-character-replacement": "Medium",
    "longest-substring-without-repeating-characters": "Medium",
    "max-consecutive-ones-iii": "Medium",
    "maximum-points-you-can-obtain-from-cards": "Medium",
    "permutation-in-string": "Medium", "sliding-window-maximum": "Hard",
    "top-k-frequent-elements": "Medium", "kth-largest-element-in-an-array": "Medium",
    "kth-largest-element-in-a-stream": "Easy", "find-median-from-data-stream": "Hard",
    "task-scheduler": "Medium", "design-twitter": "Medium",
    "k-closest-points-to-origin": "Medium", "last-stone-weight": "Easy",
    "jump-game": "Medium", "jump-game-ii": "Medium", "gas-station": "Medium",
    "merge-intervals": "Medium", "insert-interval": "Medium",
    "non-overlapping-intervals": "Medium", "valid-parenthesis-string": "Medium",
    "candy": "Hard", "assign-cookies": "Easy",
    "maximum-depth-of-binary-tree": "Easy", "invert-binary-tree": "Easy",
    "diameter-of-binary-tree": "Easy", "balanced-binary-tree": "Easy",
    "same-tree": "Easy", "subtree-of-another-tree": "Easy",
    "binary-tree-maximum-path-sum": "Hard", "binary-tree-right-side-view": "Medium",
    "binary-tree-level-order-traversal": "Medium",
    "lowest-common-ancestor-of-a-binary-search-tree": "Medium",
    "kth-smallest-element-in-a-bst": "Medium",
    "validate-binary-search-tree": "Medium",
    "construct-binary-tree-from-preorder-and-inorder-traversal": "Medium",
    "serialize-and-deserialize-binary-tree": "Hard",
    "convert-sorted-array-to-binary-search-tree": "Easy",
    "count-good-nodes-in-binary-tree": "Medium",
    "search-in-a-binary-search-tree": "Easy",
    "implement-trie-prefix-tree": "Medium",
    "design-add-and-search-words-data-structure": "Medium",
    "word-search-ii": "Hard",
    "rotting-oranges": "Medium", "number-of-provinces": "Medium",
    "accounts-merge": "Medium", "alien-dictionary": "Hard",
    "course-schedule": "Medium", "course-schedule-ii": "Medium",
    "surrounded-regions": "Medium", "flood-fill": "Easy",
    "cheapest-flights-within-k-stops": "Medium", "network-delay-time": "Medium",
    "word-ladder": "Hard", "word-ladder-ii": "Hard",
    "number-of-islands": "Medium", "clone-graph": "Medium",
    "pacific-atlantic-water-flow": "Medium", "max-area-of-island": "Medium",
    "redundant-connection": "Medium", "walls-and-gates": "Medium",
    "graph-valid-tree": "Medium",
    "number-of-connected-components-in-an-undirected-graph": "Medium",
    "reconstruct-itinerary": "Hard", "min-cost-to-connect-all-points": "Medium",
    "swim-in-rising-water": "Hard", "minimum-height-trees": "Medium",
    "01-matrix": "Medium",
    "climbing-stairs": "Easy", "house-robber": "Medium", "house-robber-ii": "Medium",
    "unique-paths": "Medium", "unique-paths-ii": "Medium",
    "edit-distance": "Medium", "longest-common-subsequence": "Medium",
    "distinct-subsequences": "Hard", "burst-balloons": "Hard",
    "wildcard-matching": "Hard", "word-break": "Medium",
    "longest-palindromic-subsequence": "Medium",
    "partition-equal-subset-sum": "Medium", "coin-change": "Medium",
    "target-sum": "Medium", "coin-change-ii": "Medium",
    "best-time-to-buy-and-sell-stock-ii": "Medium",
    "best-time-to-buy-and-sell-stock-iii": "Hard",
    "best-time-to-buy-and-sell-stock-iv": "Hard",
    "best-time-to-buy-and-sell-stock-with-cooldown": "Medium",
    "best-time-to-buy-and-sell-stock-with-transaction-fee": "Medium",
    "longest-increasing-subsequence": "Medium", "decode-ways": "Medium",
    "min-cost-climbing-stairs": "Easy", "palindromic-substrings": "Medium",
    "regular-expression-matching": "Hard",
    "interleaving-string": "Medium",
    "longest-increasing-path-in-a-matrix": "Hard",
    "maximum-subarray": "Medium",
    "hand-of-straights": "Medium",
    "merge-triplets-to-form-target-triplet": "Medium",
    "partition-labels": "Medium",
    "meeting-rooms": "Easy", "meeting-rooms-ii": "Medium",
    "minimum-interval-to-include-each-query": "Hard",
    "rotate-image": "Medium", "spiral-matrix": "Medium",
    "happy-number": "Easy", "plus-one": "Easy", "pow-x-n": "Medium",
    "multiply-strings": "Medium", "detect-squares": "Medium",
    "valid-palindrome": "Easy", "longest-palindrome": "Easy",
    "find-all-anagrams-in-a-string": "Medium",
    "group-anagrams": "Medium",
    "encode-and-decode-strings": "Medium",
    "valid-sudoku": "Medium",
    "two-sum-ii-input-array-is-sorted": "Medium",
    "first-bad-version": "Easy",
    "time-based-key-value-store": "Medium",
    "maximum-profit-in-job-scheduling": "Hard",
    "add-binary": "Easy",
    "asteroid-collision": "Medium",
    "next-permutation": "Medium",
    "contiguous-array": "Medium",
    "grumpy-bookstore-owner": "Medium",
    "largest-odd-num-in-string": "Easy",
    "maximal-rectangle": "Hard",
}

# ─── Canonical topic for each problem ───
# Primary topic assignment for the problems/ directory

TOPIC_OVERRIDES = {
    # Problems that appear in multiple topics — assign primary
    "merge-k-sorted-lists": "linked-list",
    "word-break": "dynamic-programming",
    "word-search": "backtracking",
    "coin-change": "dynamic-programming",
    "sliding-window-maximum": "sliding-window",
    "merge-intervals": "intervals",
    "insert-interval": "intervals",
    "non-overlapping-intervals": "intervals",
    "valid-parentheses": "stacks-queues",
    "trapping-rain-water": "two-pointers",
    "rotate-image": "arrays",
    "spiral-matrix": "arrays",
    "set-matrix-zeroes": "arrays",
    "maximum-subarray": "arrays",
    "best-time-to-buy-and-sell-stock": "arrays",
    "implement-trie-prefix-tree": "tries",
    "design-add-and-search-words-data-structure": "tries",
    "word-search-ii": "tries",
}


def canonical_id(raw_id: str) -> str:
    """Convert raw problem ID to canonical slug."""
    low = raw_id.lower()
    return STRIVER_TO_CANONICAL.get(low, low)


def name_from_id(pid: str) -> str:
    """Convert slug to title case name."""
    return pid.replace("-", " ").title()


def main():
    # 1. Read all sheets and collect unique problems
    all_problems = {}  # canonical_id -> {id, name, difficulty, first_topic}
    sheet_data = {}

    for sheet_file in sorted(SHEETS_DIR.glob("*.json")):
        with open(sheet_file) as f:
            data = json.load(f)
        sheet_name = sheet_file.stem

        new_data = {}
        for topic, probs in data.items():
            new_probs = []
            for raw in probs:
                cid = canonical_id(raw)
                new_probs.append(cid)

                if cid not in all_problems:
                    all_problems[cid] = {
                        "id": cid,
                        "name": name_from_id(cid),
                        "difficulty": KNOWN_DIFFICULTY.get(cid, ""),
                        "first_topic": topic,
                        "first_sheet": sheet_name,
                    }
            # Deduplicate within a topic (e.g., striver maps two IDs to same canonical)
            seen = set()
            deduped = []
            for p in new_probs:
                if p not in seen:
                    seen.add(p)
                    deduped.append(p)
            new_data[topic] = deduped

        sheet_data[sheet_name] = new_data

    # 2. Assign each problem to a canonical topic for problems/ directory
    TOPIC_MAP = {
        # Striver topic names
        "Step 01 - Basics": "basics",
        "Step 02 - Sorting Techniques": "sorting",
        "Step 03 - Arrays": "arrays",
        "Step 04 - Binary Search": "binary-search",
        "Step 05 + 18 - Strings": "strings",
        "Step 06 - Linked List": "linked-list",
        "Step 07 - Recursion": "backtracking",
        "Step 08 - Bit Manipulation": "bit-manipulation",
        "Step 09 - Stacks Queues": "stacks-queues",
        "Step 10 - Sliding Window": "sliding-window",
        "Step 11 - Heaps": "heaps",
        "Step 12 - Greedy Algorithm": "greedy",
        "Step 13 + 14 - Trees + BST": "trees",
        "Step 15 - Graphs": "graphs",
        "Step 16 - Dynamic Programming": "dynamic-programming",
        "Step 17 - Tries": "tries",
        # Blind 75 / NeetCode / Grind 75 topic names
        "Array": "arrays", "Arrays & Hashing": "arrays",
        "Binary": "bit-manipulation", "Bit Manipulation": "bit-manipulation",
        "Dynamic Programming": "dynamic-programming",
        "1-D Dynamic Programming": "dynamic-programming",
        "2-D Dynamic Programming": "dynamic-programming",
        "Graph": "graphs", "Graphs": "graphs", "Advanced Graphs": "graphs",
        "Interval": "intervals", "Intervals": "intervals",
        "Linked List": "linked-list",
        "Matrix": "arrays",
        "String": "strings",
        "Tree": "trees", "Trees": "trees",
        "Heap": "heaps", "Heap / Priority Queue": "heaps",
        "Stack": "stacks-queues",
        "Two Pointers": "two-pointers",
        "Sliding Window": "sliding-window",
        "Binary Search": "binary-search",
        "Backtracking": "backtracking",
        "Recursion": "backtracking",
        "Tries": "tries", "Trie": "tries",
        "Greedy": "greedy",
        "Math & Geometry": "math-geometry",
    }

    # Assign canonical topic
    problems_by_topic = {}
    for pid, pdata in all_problems.items():
        if pid in TOPIC_OVERRIDES:
            topic = TOPIC_OVERRIDES[pid]
        else:
            topic = TOPIC_MAP.get(pdata["first_topic"], "misc")
        if topic not in problems_by_topic:
            problems_by_topic[topic] = {}
        problems_by_topic[topic][pid] = pdata

    # 3. Load existing enriched data and merge
    enriched_path = ENRICHED_DIR / "dp_problems.json"
    enriched_by_id = {}
    if enriched_path.exists():
        with open(enriched_path) as f:
            enriched_list = json.load(f)
        for p in enriched_list:
            enriched_by_id[p["id"]] = p

    # 4. Write problems/ files
    PROBLEMS_DIR.mkdir(exist_ok=True)
    for topic, probs in sorted(problems_by_topic.items()):
        topic_problems = []
        for pid in sorted(probs.keys()):
            pdata = probs[pid]
            # Check if we have enriched data
            if pid in enriched_by_id:
                entry = enriched_by_id[pid]
            else:
                entry = {
                    "id": pid,
                    "name": pdata["name"],
                    "difficulty": pdata["difficulty"],
                    "description": "",
                    "examples": [],
                    "constraints": "",
                    "python_template": f"# {pdata['name']}\n\ndef solve():\n    pass\n",
                    "go_template": f"// {pdata['name']}\n\npackage main\n\nfunc solve() {{\n\n}}\n",
                }
                # Ensure difficulty from our known map
                if not entry.get("difficulty"):
                    entry["difficulty"] = KNOWN_DIFFICULTY.get(pid, "")
            topic_problems.append(entry)

        with open(PROBLEMS_DIR / f"{topic}.json", "w") as f:
            json.dump(topic_problems, f, indent=2)
        print(f"  problems/{topic}.json: {len(topic_problems)} problems")

    # 5. Write updated sheet files
    for sheet_name, data in sheet_data.items():
        with open(SHEETS_DIR / f"{sheet_name}.json", "w") as f:
            json.dump(data, f, indent=2)
        total = sum(len(v) for v in data.values())
        print(f"  sheets/{sheet_name}.json: {total} problems (canonical IDs)")

    # 6. Summary
    total_unique = len(all_problems)
    with_difficulty = sum(1 for p in all_problems.values() if p["difficulty"])
    print(f"\n  Total unique problems: {total_unique}")
    print(f"  With difficulty: {with_difficulty}")
    print(f"  Without difficulty: {total_unique - with_difficulty}")
    print(f"  Topics: {len(problems_by_topic)}")
    print(f"\n  Done! You can now delete enriched/ directory.")


if __name__ == "__main__":
    main()
