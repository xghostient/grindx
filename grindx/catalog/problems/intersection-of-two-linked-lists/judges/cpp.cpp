#include "_common.h"
#include "solution.cpp"

static ListNode* build_list(const json::Array& arr) {
    return list_to_linked_list(arr);
}

static ListNode* tail(ListNode* head) {
    while (head && head->next) head = head->next;
    return head;
}

static std::tuple<ListNode*, ListNode*, ListNode*> build_intersection(const json::Array& a, const json::Array& b, const json::Array& shared) {
    ListNode* shared_head = build_list(shared);
    ListNode* head_a = build_list(a);
    ListNode* head_b = build_list(b);
    if (!head_a) head_a = shared_head;
    else if (shared_head) tail(head_a)->next = shared_head;
    if (!head_b) head_b = shared_head;
    else if (shared_head) tail(head_b)->next = shared_head;
    return {head_a, head_b, shared_head};
}

int main() {
    auto tc = load_cases("intersection-of-two-linked-lists");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto built = build_intersection(c["input"][0].get_array(), c["input"][1].get_array(), c["input"][2].get_array());
        ListNode* result = getIntersectionNode(std::get<0>(built), std::get<1>(built));
        if (result != std::get<2>(built)) {
            json::Value actual(linked_list_to_list(result));
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), c["expected"].to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
