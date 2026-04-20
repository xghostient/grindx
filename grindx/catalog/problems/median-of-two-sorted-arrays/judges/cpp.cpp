    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("median-of-two-sorted-arrays");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto nums1 = cases[i]["input"][0].get<std::vector<int>>();
    auto nums2 = cases[i]["input"][1].get<std::vector<int>>();
    double actual = findMedianSortedArrays(nums1, nums2);
    double expected = cases[i]["expected"].get<double>();
    if (std::abs(actual - expected) > 1e-5) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
