        #include "_common.h"
        #include "solution.cpp"



        int main() {
            auto tc = load_cases("count-and-say");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    int n = c["input"][0].get_int();
    std::string actual = countAndSay(n);
    std::string expected = c["expected"].get_string();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), expected, actual, total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

            report_ac(total);
        }
