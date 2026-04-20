    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("lis-03-largest-div-subset");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    auto arr = c["input"][0].get<std::vector<int>>();
    auto actual = largestDivisibleSubset(arr);
    int expected = c["expected"].get<int>();
    std::set<int> input_set(arr.begin(), arr.end());
    std::set<int> actual_set(actual.begin(), actual.end());
    bool valid = static_cast<int>(actual.size()) == expected && actual_set.size() == actual.size();
    if (valid) {
        for (int value : actual) {
            if (!input_set.count(value)) valid = false;
        }
    }
    if (valid) {
        for (size_t x = 0; x < actual.size(); x++) {
            for (size_t y = x + 1; y < actual.size(); y++) {
                if (actual[x] % actual[y] != 0 && actual[y] % actual[x] != 0) valid = false;
            }
        }
    }
    if (!valid) {
        report_wa(i, c["input"].to_string(), std::string("valid divisible subset length ") + std::to_string(expected), json::Value(actual).to_string(), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
