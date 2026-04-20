    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("multiply-strings");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto num1 = cases[i]["input"][0].get_string();
    auto num2 = cases[i]["input"][1].get_string();
    std::string actual = multiply(num1, num2);
    auto expected = cases[i]["expected"].get_string();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected, actual, total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
