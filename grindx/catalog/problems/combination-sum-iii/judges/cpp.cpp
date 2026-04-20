        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> normalize_int_matrix(std::vector<std::vector<int>> values) {
    for (auto& row : values) std::sort(row.begin(), row.end());
    std::sort(values.begin(), values.end());
    return values;
}

static std::string int_matrix_to_string(const std::vector<std::vector<int>>& matrix) {
    json::Array rows;
    for (const auto& row : matrix) {
        json::Array arr;
        for (int value : row) arr.push_back(json::Value(value));
        rows.push_back(json::Value(arr));
    }
    return json::Value(rows).to_string();
}


        int main() {
            auto tc = load_cases("combination-sum-iii");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        int k = cases[i]["input"][0].get<int>();
        int n = cases[i]["input"][1].get<int>();
        auto actual = normalize_int_matrix(combinationSum3(k, n));
        auto expected = cases[i]["expected"].get<std::vector<std::vector<int>>>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), int_matrix_to_string(expected), int_matrix_to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
