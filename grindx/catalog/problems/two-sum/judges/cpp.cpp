/**
 * Judge for Two Sum — function pattern, unordered comparison.
 */

#include "_common.h"
#include "solution.cpp"

#include <sstream>

namespace {

struct LargeCase {
    std::vector<int> nums;
    int target;
    std::vector<int> expected_indices;
};

std::string vector_to_string(const std::vector<int>& values) {
    json::Array arr;
    for (int value : values) {
        arr.push_back(json::Value(value));
    }
    return json::Value(arr).to_string();
}

bool valid_index_pair(const std::vector<int>& result, int size) {
    if (result.size() != 2) {
        return false;
    }
    for (int idx : result) {
        if (idx < 0 || idx >= size) {
            return false;
        }
    }
    return true;
}

std::vector<LargeCase> generate_large_cases() {
    constexpr int n = 10000;
    std::vector<LargeCase> cases;
    cases.reserve(4);

    {
        std::vector<int> nums(n);
        nums[0] = -500000000;
        for (int i = 1; i < n - 1; i++) {
            nums[i] = 200000000 + ((i * 7919) % 700000000);
        }
        nums[n - 1] = 123456789;
        cases.push_back({nums, -376543211, {0, n - 1}});
    }

    {
        std::vector<int> nums(n);
        for (int i = 0; i < n; i++) {
            nums[i] = 300000000 + ((i * 1237) % 600000000);
        }
        int dup_i = 137;
        int dup_j = 9862;
        nums[dup_i] = 123456789;
        nums[dup_j] = 123456789;
        cases.push_back({nums, 246913578, {dup_i, dup_j}});
    }

    {
        std::vector<int> nums(n);
        for (int i = 0; i < n; i++) {
            nums[i] = 1 + ((i * 48271) % 999999998);
        }
        int low_i = 4000;
        int high_i = 7000;
        nums[low_i] = -1000000000;
        nums[high_i] = 1000000000;
        cases.push_back({nums, 0, {low_i, high_i}});
    }

    {
        std::vector<int> nums(n);
        for (int i = 0; i < n; i++) {
            nums[i] = 1 + ((i * 8191) % 999999999);
        }
        int zero_i = 2500;
        int zero_j = 7500;
        nums[zero_i] = 0;
        nums[zero_j] = 0;
        cases.push_back({nums, 0, {zero_i, zero_j}});
    }

    return cases;
}

}  // namespace

int main() {
    auto tc = load_cases("two-sum");
    auto& cases = tc["cases"].get_array();

    auto large_cases = generate_large_cases();

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto nums = c["input"][0].get<std::vector<int>>();
        int target = c["input"][1].get<int>();

        auto result = twoSum(nums, target);

        auto expected = c["expected"].get<std::vector<int>>();

        if (!valid_index_pair(result, static_cast<int>(nums.size()))) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), c["expected"].to_string(),
                vector_to_string(result), total, cat);
        }

        if (!compare_unordered(result, expected)) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), c["expected"].to_string(),
                vector_to_string(result), total, cat);
        }
        report_progress(i + 1, total);
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];
        auto nums_copy = lc.nums;
        auto result = twoSum(nums_copy, lc.target);

        if (!valid_index_pair(result, static_cast<int>(lc.nums.size()))) {
            report_wa(idx, "large input", vector_to_string(lc.expected_indices),
                vector_to_string(result), total, "tle");
        }

        if (!compare_unordered(result, lc.expected_indices)) {
            report_wa(idx, "large input", vector_to_string(lc.expected_indices),
                vector_to_string(result), total, "tle");
        }
    }

    report_ac(total);
}
