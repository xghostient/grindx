#include "_common.h"
#include "solution.cpp"

static std::pair<ListNode*, std::vector<ListNode*>> build_cycle(const json::Array& arr, int pos) {
    if (arr.empty()) return {nullptr, {}};
    std::vector<ListNode*> nodes;
    ListNode* head = new ListNode(arr[0].get_int());
    nodes.push_back(head);
    ListNode* cur = head;
    for (size_t i = 1; i < arr.size(); i++) {
        cur->next = new ListNode(arr[i].get_int());
        cur = cur->next;
        nodes.push_back(cur);
    }
    if (pos >= 0) cur->next = nodes[pos];
    return {head, nodes};
}

int main() {
    auto tc = load_cases("linked-list-cycle-ii");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto built = build_cycle(c["input"][0].get_array(), c["input"][1].get<int>());
        ListNode* result = detectCycle(built.first);
        int actual = -1;
        for (int idx = 0; idx < static_cast<int>(built.second.size()); idx++) {
            if (result == built.second[idx]) {
                actual = idx;
                break;
            }
        }
        int expected = c["expected"].get<int>();
        if (actual != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
