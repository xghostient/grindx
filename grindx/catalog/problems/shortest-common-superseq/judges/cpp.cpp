    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("shortest-common-superseq");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        auto is_subsequence = [](const std::string& needle, const std::string& haystack) {
    size_t idx = 0;
    for (char ch : haystack) {
        if (idx < needle.size() && needle[idx] == ch) {
            idx++;
        }
    }
    return idx == needle.size();
};

for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    std::string a = c["input"][0].get<std::string>();
    std::string b = c["input"][1].get<std::string>();
    std::string actual = shortestCommonSupersequence(a, b);
    int expected = c["expected"].get<int>();
    if (static_cast<int>(actual.size()) != expected || !is_subsequence(a, actual) || !is_subsequence(b, actual)) {
        report_wa(i, c["input"].to_string(), std::string("valid shortest supersequence length ") + std::to_string(expected), actual, total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

        report_ac(total);
    }
