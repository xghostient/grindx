        #include "_common.h"
        #include "solution.cpp"

        static std::string to_string_matrix(const std::vector<std::vector<int>>& matrix) {
    json::Array rows;
    for (const auto& row : matrix) {
        json::Array arr;
        for (int value : row) arr.push_back(json::Value(value));
        rows.push_back(json::Value(arr));
    }
    return json::Value(rows).to_string();
}


        int main() {
            auto tc = load_cases("non-overlapping-intervals");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto intervals = cases[i]["input"][0].get<std::vector<std::vector<int>>>();
        int actual = eraseOverlapIntervals(intervals);
        int expected = cases[i]["expected"].get<int>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
