        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<std::string>> normalize_str_matrix(std::vector<std::vector<std::string>> values) {
    std::sort(values.begin(), values.end());
    return values;
}

static std::string str_matrix_to_string(const std::vector<std::vector<std::string>>& matrix) {
    json::Array rows;
    for (const auto& row : matrix) {
        json::Array arr;
        for (const auto& s : row) arr.push_back(json::Value(s));
        rows.push_back(json::Value(arr));
    }
    return json::Value(rows).to_string();
}


        int main() {
            auto tc = load_cases("n-queens");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        int n = cases[i]["input"][0].get<int>();
        auto actual = normalize_str_matrix(solveNQueens(n));
        auto expected = cases[i]["expected"].get<std::vector<std::vector<std::string>>>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), str_matrix_to_string(expected), str_matrix_to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
