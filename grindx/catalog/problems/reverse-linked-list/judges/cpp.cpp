/**
 * Judge for Reverse Linked List — function pattern, linked list I/O.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("reverse-linked-list");
    auto& cases = tc["cases"].get_array();

    // Generate a max-constraint hidden case within the published bounds.
    struct LargeCase {
        std::vector<int> vals;
    };
    std::vector<LargeCase> large_cases;
    {
        std::vector<int> vals(5000);
        for (int k = 0; k < 5000; k++) vals[k] = ((k * 73) % 1001) - 500;
        large_cases.push_back({vals});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto& arr = c["input"][0].get_array();
        ListNode* head = list_to_linked_list(arr);

        ListNode* result = reverseList(head);

        json::Array result_arr = linked_list_to_list(result);
        json::Value result_val(result_arr);
        json::Value expected_val(c["expected"].get_array());

        if (result_val.to_string() != expected_val.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected_val.to_string(),
                result_val.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];

        // Build linked list
        json::Array input_arr;
        for (int v : lc.vals) input_arr.push_back(json::Value(v));
        ListNode* head = list_to_linked_list(input_arr);

        ListNode* result = reverseList(head);

        // Verify: result should be the reverse of input
        json::Array result_arr = linked_list_to_list(result);
        json::Array expected_arr;
        for (int k = static_cast<int>(lc.vals.size()) - 1; k >= 0; k--) {
            expected_arr.push_back(json::Value(lc.vals[k]));
        }
        json::Value result_val(result_arr);
        json::Value expected_val(expected_arr);
        if (result_val.to_string() != expected_val.to_string()) {
            report_wa(idx, "max input (5000 elements)", expected_val.to_string(),
                result_val.to_string(), total, "stress");
        }
    }

    report_ac(total);
}
