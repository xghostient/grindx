    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("add-binary");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto a = cases[i]["input"][0].get<std::string>();
    auto b = cases[i]["input"][1].get<std::string>();
    auto actual = addBinary(a, b);
    auto expected = cases[i]["expected"].get<std::string>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected, actual, total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
