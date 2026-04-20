    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("wildcard-matching");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    std::string a = c["input"][0].get<std::string>();
    std::string b = c["input"][1].get<std::string>();
    bool actual = isMatch(a, b);
    bool expected = c["expected"].get<bool>();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
