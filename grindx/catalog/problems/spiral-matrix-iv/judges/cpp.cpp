#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("spiral-matrix-iv");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());

    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        int arg0 = c["input"][0].get<int>();
        int arg1 = c["input"][1].get<int>();
        auto arg2 = list_to_linked_list(c["input"][2].get_array());
        auto expected = c["expected"].get<std::vector<std::vector<int>>>();

                std::vector<std::vector<int>> result = spiralMatrix(arg0, arg1, arg2);
                auto actual = result;
        if (actual != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), grindx_matrix_to_string(expected), grindx_matrix_to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    report_ac(total);
}
