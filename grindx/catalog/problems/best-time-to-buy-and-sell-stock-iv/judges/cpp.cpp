    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("best-time-to-buy-and-sell-stock-iv");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    int a = c["input"][0].get<int>();
    auto nums = c["input"][1].get<std::vector<int>>();
    int actual = maxProfit(a, nums);
    int expected = c["expected"].get<int>();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
