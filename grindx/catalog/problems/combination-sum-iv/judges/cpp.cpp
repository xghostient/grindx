    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("combination-sum-iv");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    auto nums = c["input"][0].get<std::vector<int>>();
    int target = c["input"][1].get<int>();
    int actual = combinationSum4(nums, target);
    int expected = c["expected"].get<int>();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
