    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("lis-02-print-lis");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        auto is_subsequence_list = [](const std::vector<int>& seq, const std::vector<int>& arr) {
    size_t idx = 0;
    for (int value : arr) {
        if (idx < seq.size() && seq[idx] == value) idx++;
    }
    return idx == seq.size();
};

for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    auto arr = c["input"][0].get<std::vector<int>>();
    auto actual = printLIS(arr);
    int expected = c["expected"].get<int>();
    bool valid = static_cast<int>(actual.size()) == expected;
    if (valid) {
        for (size_t j = 0; j + 1 < actual.size(); j++) {
            if (actual[j] >= actual[j + 1]) valid = false;
        }
        if (valid && !is_subsequence_list(actual, arr)) valid = false;
    }
    if (!valid) {
        report_wa(i, c["input"].to_string(), std::string("valid LIS length ") + std::to_string(expected), json::Value(actual).to_string(), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

        report_ac(total);
    }
