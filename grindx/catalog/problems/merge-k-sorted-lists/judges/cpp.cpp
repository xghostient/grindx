/**
 * Judge for Merge K Sorted Lists — function pattern, linked list I/O.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("merge-k-sorted-lists");
    auto& cases = tc["cases"].get_array();

    // Generate dense and sparse hidden cases at the published bounds.
    struct LargeCase {
        std::vector<std::vector<int>> lists;
    };
    std::vector<LargeCase> large_cases;
    {
        std::vector<std::vector<int>> lists(100);
        for (int i = 0; i < 100; i++) {
            lists[i].resize(100);
            for (int k = 0; k < 100; k++) lists[i][k] = (((i * 97) + (k * 29)) % 20001) - 10000;
            std::sort(lists[i].begin(), lists[i].end());
        }
        large_cases.push_back({lists});
    }
    {
        std::vector<std::vector<int>> lists(10000);
        for (int i = 0; i < 10000; i++) {
            lists[i].push_back(((i * 37) % 20001) - 10000);
        }
        large_cases.push_back({lists});
    }
    {
        std::vector<std::vector<int>> lists(10000);
        lists[123] = {-5, -5, 0, 3};
        lists[5000] = {-1, 2, 2};
        lists[9999] = {4};
        large_cases.push_back({lists});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto& input_lists = c["input"][0].get_array();

        // Deserialize each sub-array to a ListNode*
        std::vector<ListNode*> lists;
        for (size_t j = 0; j < input_lists.size(); j++) {
            auto& sub = input_lists[j].get_array();
            lists.push_back(list_to_linked_list(sub));
        }

        ListNode* result = mergeKLists(lists);

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

        // Build vector of linked lists
        std::vector<ListNode*> lists;
        for (auto& sub_vals : lc.lists) {
            json::Array sub_arr;
            for (int v : sub_vals) sub_arr.push_back(json::Value(v));
            lists.push_back(list_to_linked_list(sub_arr));
        }

        ListNode* result = mergeKLists(lists);

        // Verify: result should be sorted merge of all lists
        json::Array result_arr = linked_list_to_list(result);
        std::vector<int> merged;
        for (auto& sub_vals : lc.lists) {
            merged.insert(merged.end(), sub_vals.begin(), sub_vals.end());
        }
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
