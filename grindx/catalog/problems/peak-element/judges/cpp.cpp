    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("peak-element");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto nums = cases[i]["input"][0].get<std::vector<int>>();
    int idx = findPeakElement(nums);
    int n = static_cast<int>(nums.size());
    bool valid = idx >= 0 && idx < n;
    if (valid && idx > 0 && nums[idx] <= nums[idx - 1]) valid = false;
    if (valid && idx < n - 1 && nums[idx] <= nums[idx + 1]) valid = false;
    if (!valid) report_wa(i, cases[i]["input"].to_string(), "valid peak", std::to_string(idx), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
