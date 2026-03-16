/**
 * Judge for Rotate Array — in-place mutation pattern.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("rotate-array");
    auto& cases = tc["cases"].get_array();

    // Generate large cases for TLE detection
    struct LargeCase {
        std::vector<int> nums;
        int k;
        std::vector<int> expected;
    };
    std::vector<LargeCase> large_cases;
    std::mt19937 rng(42);
    for (int n : {100000}) {
        std::vector<int> nums(n);
        std::uniform_int_distribution<int> dist(-1000000000, 1000000000);
        for (int i = 0; i < n; i++) nums[i] = dist(rng);
        int k = static_cast<int>(rng() % n);
        // Compute expected by simple rotation
        std::vector<int> expected(n);
        for (int i = 0; i < n; i++) {
            expected[(i + k) % n] = nums[i];
        }
        large_cases.push_back({nums, k, expected});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto nums = c["input"][0].get<std::vector<int>>();
        int k = c["input"][1].get<int>();

        rotate(nums, k);

        auto expected = c["expected"].get<std::vector<int>>();

        if (nums != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            json::Array result_arr;
            for (int v : nums) result_arr.push_back(json::Value(v));
            report_wa(i, c["input"].to_string(), c["expected"].to_string(),
                json::Value(result_arr).to_string(), total, cat);
        }
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];
        auto nums_copy = lc.nums;

        rotate(nums_copy, lc.k);

        if (nums_copy != lc.expected) {
            json::Array result_arr;
            for (int v : nums_copy) result_arr.push_back(json::Value(v));
            report_wa(idx, "large input (100000 elements)",
                "rotated array",
                truncate(json::Value(result_arr).to_string()),
                total, "tle");
        }
    }

    report_ac(total);
}
