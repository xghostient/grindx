#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("combination-sum");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());

    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        int arg1 = c["input"][1].get<int>();
        auto expected = c["expected"].get<std::vector<std::vector<int>>>();

                std::vector<std::vector<int>> result = combinationSum(arg0, arg1);
                auto actual = result;
        if (!compare_unordered_nested(actual, expected)) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), grindx_matrix_to_string(expected), grindx_matrix_to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    report_ac(total);
}
