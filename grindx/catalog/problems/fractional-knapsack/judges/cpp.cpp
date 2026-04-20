    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("fractional-knapsack");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto values = cases[i]["input"][0].get<std::vector<int>>();
    auto weights = cases[i]["input"][1].get<std::vector<int>>();
    int cap = cases[i]["input"][2].get<int>();
    double actual = fractionalKnapsack(values, weights, cap);
    double expected = cases[i]["expected"].get<double>();
    if (std::abs(actual - expected) > 1e-4) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
