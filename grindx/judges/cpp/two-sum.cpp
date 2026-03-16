/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("two-sum");
    auto& cases = tc["cases"].get_array();

    // Generate large cases for TLE detection
    struct LargeCase {
        std::vector<int> nums;
        int target;
    };
    std::vector<LargeCase> large_cases;
    std::mt19937 rng(42);
    for (int n : {10000, 100000}) {
        std::vector<int> nums(n);
        std::uniform_int_distribution<int> dist(-1000000000, 1000000000);
        for (int k = 0; k < n; k++) nums[k] = dist(rng);
        int i = rng() % n;
        int j = rng() % n;
        while (j == i) j = (j + 1) % n;
        int target = nums[i] + nums[j];
        large_cases.push_back({nums, target});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto nums = c["input"][0].get<std::vector<int>>();
        int target = c["input"][1].get<int>();

        auto result = twoSum(nums, target);

        auto expected = c["expected"].get<std::vector<int>>();

        if (!compare_unordered(result, expected)) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), c["expected"].to_string(),
                json::Value(json::Array(result.begin(), result.end())).to_string(),
                total, cat);
        }
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];
        auto nums_copy = lc.nums;
        auto result = twoSum(nums_copy, lc.target);

        if (result.size() != 2 || result[0] == result[1] ||
            lc.nums[result[0]] + lc.nums[result[1]] != lc.target) {
            report_wa(idx, "large input", std::to_string(lc.target),
                "[" + std::to_string(result[0]) + "," + std::to_string(result[1]) + "]",
                total, "tle");
        }
    }

    report_ac(total);
}
