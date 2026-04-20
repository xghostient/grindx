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
            auto tc = load_cases("remove-duplicates-from-sorted-array");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto nums = cases[i]["input"][0].get<std::vector<int>>();
        int actual_k = removeDuplicates(nums);
        int expected_k = cases[i]["expected"]["k"].get<int>();
        auto expected_prefix = cases[i]["expected"]["prefix"].get<std::vector<int>>();
        std::vector<int> actual_prefix;
        if (actual_k >= 0 && actual_k <= static_cast<int>(nums.size())) actual_prefix.assign(nums.begin(), nums.begin() + actual_k);
        if (actual_k != expected_k || actual_prefix != expected_prefix) {
            json::Object actual_obj;
            actual_obj["k"] = json::Value(actual_k);
            json::Array prefix_arr;
            for (int value : actual_prefix) prefix_arr.push_back(json::Value(value));
            actual_obj["prefix"] = json::Value(prefix_arr);
            report_wa(i, cases[i]["input"].to_string(), cases[i]["expected"].to_string(), json::Value(actual_obj).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        }
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
