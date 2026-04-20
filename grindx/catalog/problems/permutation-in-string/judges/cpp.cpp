        #include "_common.h"
        #include "solution.cpp"

        static bool is_valid_min_window(const std::string& source, const std::string& target, const std::string& expected, const std::string& actual) {
    if (actual.size() != expected.size()) return false;
    if (expected.empty()) return actual.empty();
    if (source.find(actual) == std::string::npos) return false;
    std::unordered_map<char, int> need;
    std::unordered_map<char, int> have;
    for (char ch : target) need[ch]++;
    for (char ch : actual) have[ch]++;
    for (const auto& [ch, count] : need) {
        if (have[ch] < count) return false;
    }
    return true;
}


        int main() {
            auto tc = load_cases("permutation-in-string");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        std::string a = cases[i]["input"][0].get<std::string>();
        std::string b = cases[i]["input"][1].get<std::string>();
        bool actual = checkInclusion(a, b);
        bool expected = cases[i]["expected"].get<bool>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
