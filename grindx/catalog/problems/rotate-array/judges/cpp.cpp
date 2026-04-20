/**
 * Judge for Rotate Array — in-place mutation pattern.
 */

#include "_common.h"
#include "solution.cpp"

namespace {

struct LargeCase {
    std::vector<int> nums;
    int k;
    std::vector<int> expected;
};

std::vector<int> rotate_expected(const std::vector<int>& nums, int k) {
    int n = static_cast<int>(nums.size());
    int effective = k % n;
    if (effective == 0) {
        return nums;
    }
    std::vector<int> expected;
    expected.reserve(n);
    expected.insert(expected.end(), nums.end() - effective, nums.end());
    expected.insert(expected.end(), nums.begin(), nums.end() - effective);
    return expected;
}

std::vector<LargeCase> generate_large_cases() {
    std::vector<LargeCase> cases;
    cases.reserve(8);
    for (const std::array<int, 4>& spec : {
             std::array<int, 4>{100000, 99999, -1000000000, 37},
             std::array<int, 4>{100000, 87500, -999900000, 53},
             std::array<int, 4>{100000, 75000, -999800000, 61},
             std::array<int, 4>{100000, 62500, -999700000, 73},
             std::array<int, 4>{100000, 50000, -999600000, 79},
             std::array<int, 4>{100000, 37500, -999500000, 83},
             std::array<int, 4>{100000, 25000, -999400000, 89},
             std::array<int, 4>{99999, 99998, -999300000, 97},
         }) {
        int n = spec[0];
        int k = spec[1];
        int start = spec[2];
        int step = spec[3];
        std::vector<int> nums(n);
        for (int i = 0; i < n; i++) {
            nums[i] = start + (i * step);
        }
        cases.push_back({nums, k, rotate_expected(nums, k)});
    }
    return cases;
}

}  // namespace

int main() {
    auto tc = load_cases("rotate-array");
    auto& cases = tc["cases"].get_array();

    auto large_cases = generate_large_cases();

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
        report_progress(i + 1, total);
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
