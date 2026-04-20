    #include "_common.h"
    #include "solution.cpp"



    int main() {
        auto tc = load_cases("remove-k-digits");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    std::string num = cases[i]["input"][0].get<std::string>();
    int k = cases[i]["input"][1].get<int>();
    std::string actual = removeKdigits(num, k);
    std::string expected = cases[i]["expected"].get<std::string>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected, actual, total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
