#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("odd-even-linked-list");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        ListNode* head = list_to_linked_list(c["input"][0].get_array());
        json::Value actual(linked_list_to_list(oddEvenList(head)));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
