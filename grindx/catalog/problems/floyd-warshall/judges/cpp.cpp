        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> clone_matrix(const std::vector<std::vector<int>>& matrix) { return matrix; }
static std::vector<std::vector<std::vector<int>>> get_int_tensor3(const json::Value& value) {
    std::vector<std::vector<std::vector<int>>> out;
    for (const auto& rowv : value.get_array()) {
        std::vector<std::vector<int>> row;
        for (const auto& edgev : rowv.get_array()) row.push_back(edgev.get<std::vector<int>>());
        out.push_back(row);
    }
    return out;
}


        int main() {
            auto tc = load_cases("floyd-warshall");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) { auto& c = cases[i]; auto matrix = c["input"][0].get<std::vector<std::vector<int>>>(); auto actual = floydWarshall(matrix); auto expected = c["expected"].get<std::vector<std::vector<int>>>(); if (actual != expected) report_wa(i, c["input"].to_string(), grindx_matrix_to_string(expected), grindx_matrix_to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    report_progress(i + 1, total);
}

            report_ac(total);
        }
