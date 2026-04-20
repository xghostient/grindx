/**
 * Judge for Merge Two Sorted Lists — function pattern, linked list I/O.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("merge-two-sorted-lists");
    auto& cases = tc["cases"].get_array();

    // Generate hidden max-constraint correctness cases.
    struct LargeCase {
        std::vector<int> vals1;
        std::vector<int> vals2;
    };
    std::vector<LargeCase> large_cases;
    {
        std::vector<int> vals2(50);
        for (int k = 0; k < 50; k++) vals2[k] = (((k * 7) + 3) % 201) - 100;
        std::sort(vals2.begin(), vals2.end());
        large_cases.push_back({{}, vals2});
    }
    {
        std::vector<int> vals1(25);
        std::vector<int> vals2(25);
        for (int k = 0; k < 25; k++) vals1[k] = (((k * 9) + 1) % 201) - 100;
        for (int k = 0; k < 25; k++) vals2[k] = (((k * 11) + 5) % 201) - 100;
        std::sort(vals1.begin(), vals1.end());
        std::sort(vals2.begin(), vals2.end());
        large_cases.push_back({vals1, vals2});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto& arr1 = c["input"][0].get_array();
        auto& arr2 = c["input"][1].get_array();
        ListNode* list1 = list_to_linked_list(arr1);
        ListNode* list2 = list_to_linked_list(arr2);

        ListNode* result = mergeTwoLists(list1, list2);

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

        // Build linked lists
        json::Array input_arr1;
        for (int v : lc.vals1) input_arr1.push_back(json::Value(v));
        ListNode* list1 = list_to_linked_list(input_arr1);

        json::Array input_arr2;
        for (int v : lc.vals2) input_arr2.push_back(json::Value(v));
        ListNode* list2 = list_to_linked_list(input_arr2);

        ListNode* result = mergeTwoLists(list1, list2);

        // Verify: result should be sorted merge of both inputs
        json::Array result_arr = linked_list_to_list(result);
        std::vector<int> merged;
        merged.insert(merged.end(), lc.vals1.begin(), lc.vals1.end());
        merged.insert(merged.end(), lc.vals2.begin(), lc.vals2.end());
        std::sort(merged.begin(), merged.end());
        json::Array expected_arr;
        for (int v : merged) expected_arr.push_back(json::Value(v));

        json::Value result_val(result_arr);
        json::Value expected_val(expected_arr);
        if (result_val.to_string() != expected_val.to_string()) {
            report_wa(idx, "hidden input", expected_val.to_string(),
                result_val.to_string(), total, "stress");
        }
    }

    report_ac(total);
}
