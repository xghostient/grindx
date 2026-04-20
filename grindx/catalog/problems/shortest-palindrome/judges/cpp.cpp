        #include "_common.h"
        #include "solution.cpp"



        int main() {
            auto tc = load_cases("shortest-palindrome");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    std::string s = c["input"][0].get_string();
    std::string actual = shortestPalindrome(s);
    std::string expected = c["expected"].get_string();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), expected, actual, total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

            report_ac(total);
        }
