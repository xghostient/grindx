#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("find-the-duplicate-number");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto nums = c["input"][0].get<std::vector<int>>();
        int actual = findDuplicate(nums);
        int expected = c["expected"].get<int>();
        if (actual != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
