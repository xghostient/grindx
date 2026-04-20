    #include "_common.h"
    #include "solution.cpp"



    int main() {
        auto tc = load_cases("sum-of-subarray-ranges");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto nums = cases[i]["input"][0].get<std::vector<int>>();
    long long actual = subArrayRanges(nums);
    long long expected = cases[i]["expected"].get<long long>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
