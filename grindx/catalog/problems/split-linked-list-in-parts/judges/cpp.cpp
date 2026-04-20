#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("split-linked-list-in-parts");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        ListNode* head = list_to_linked_list(c["input"][0].get_array());
        auto result = splitListToParts(head, c["input"][1].get<int>());
        json::Array actual;
        for (auto* node : result) actual.push_back(json::Value(linked_list_to_list(node)));
        json::Value actual_val(actual);
        json::Value expected(c["expected"].get_array());
        if (actual_val.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual_val.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
