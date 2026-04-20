    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("pow-x-n");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    double x = cases[i]["input"][0].get<double>();
    int n = cases[i]["input"][1].get<int>();
    double actual = myPow(x, n);
    double expected = cases[i]["expected"].get<double>();
    double diff = std::abs(actual - expected);
    bool pass_check = std::isfinite(actual) && (diff <= 1e-5 || diff / std::max(std::abs(expected), 1e-9) <= 1e-5);
    if (!pass_check) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
