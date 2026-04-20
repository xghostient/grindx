/**
 * Judge for Reorder List — in-place linked list modification.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("reorder-list");
    auto& cases = tc["cases"].get_array();

    // Generate large hidden cases at the published bounds.
    struct LargeCase {
        std::vector<int> vals;
    };
    std::vector<LargeCase> large_cases;
    {
        std::vector<int> vals(50000);
        for (int k = 0; k < 50000; k++) vals[k] = (k % 1000) + 1;
        large_cases.push_back({vals});
    }
    {
        std::vector<int> vals(49999);
        for (int k = 0; k < 49999; k++) vals[k] = ((k * 7) % 1000) + 1;
        large_cases.push_back({vals});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto& arr = c["input"][0].get_array();
        ListNode* head = list_to_linked_list(arr);

        reorderList(head);

        json::Array result_arr = linked_list_to_list(head);
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

        reorderList(head);

        // Verify: compute expected reorder L0->Ln->L1->Ln-1->...
        json::Array result_arr = linked_list_to_list(head);
        int n = static_cast<int>(lc.vals.size());
        json::Array expected_arr;
        int lo = 0, hi = n - 1;
        bool front = true;
        while (lo <= hi) {
            if (front) {
                expected_arr.push_back(json::Value(lc.vals[lo]));
                lo++;
            } else {
                expected_arr.push_back(json::Value(lc.vals[hi]));
                hi--;
            }
            front = !front;
        }

        json::Value result_val(result_arr);
        json::Value expected_val(expected_arr);
        if (result_val.to_string() != expected_val.to_string()) {
            report_wa(idx, "hidden input", expected_val.to_string(),
                result_val.to_string(), total, "stress");
        }
    }

    report_ac(total);
}
