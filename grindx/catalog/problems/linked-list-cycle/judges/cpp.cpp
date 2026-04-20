/**
 * Judge for Linked List Cycle — function pattern, bool comparison.
 * Builds linked lists with cycles manually (cannot use list_to_linked_list).
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

/**
 * Build a linked list from values, then create a cycle by connecting
 * the tail to the node at index `pos`. If pos < 0, no cycle is created.
 */
static ListNode* build_cyclic_list(const std::vector<int>& vals, int pos) {
    if (vals.empty()) return nullptr;
    std::vector<ListNode*> nodes;
    for (int v : vals) nodes.push_back(new ListNode(v));
    for (size_t i = 0; i + 1 < nodes.size(); i++) {
        nodes[i]->next = nodes[i + 1];
    }
    if (pos >= 0 && pos < static_cast<int>(nodes.size())) {
        nodes.back()->next = nodes[pos];
    }
    return nodes[0];
}

int main() {
    auto tc = load_cases("linked-list-cycle");
    auto& cases = tc["cases"].get_array();

    // Generate hidden max-constraint cyclic and acyclic cases.
    struct LargeCase {
        std::vector<int> vals;
        int pos;
        bool expected;
    };
    std::vector<LargeCase> large_cases;
    {
        std::vector<int> vals(10000);
        for (int k = 0; k < 10000; k++) vals[k] = ((k * 17) % 200001) - 100000;
        large_cases.push_back({vals, 5000, true});
        large_cases.push_back({vals, -1, false});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto values = c["input"][0].get<std::vector<int>>();
        int pos = c["input"][1].get<int>();

        ListNode* head = build_cyclic_list(values, pos);

        bool result = hasCycle(head);
        bool expected = c["expected"].get_bool();

        if (result != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(),
                expected ? "true" : "false",
                result ? "true" : "false",
                total, cat);
        }
        report_progress(i + 1, total);
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];

        ListNode* head = build_cyclic_list(lc.vals, lc.pos);

        bool result = hasCycle(head);

        if (result != lc.expected) {
            report_wa(idx, "hidden input (10000 nodes)",
                lc.expected ? "true" : "false",
                result ? "true" : "false",
                total, "stress");
        }
    }

    report_ac(total);
}
