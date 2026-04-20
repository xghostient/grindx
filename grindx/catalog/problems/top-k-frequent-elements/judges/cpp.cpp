        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> normalize_int_matrix(std::vector<std::vector<int>> rows) {
    for (auto& row : rows) std::sort(row.begin(), row.end());
    std::sort(rows.begin(), rows.end());
    return rows;
}

static std::vector<int> sorted_ints(std::vector<int> values) {
    std::sort(values.begin(), values.end());
    return values;
}

static std::string tasks_to_string(const std::vector<std::string>& tasks) {
    std::string out;
    out.reserve(tasks.size());
    for (const auto& task : tasks) {
        out.push_back(task.empty() ? '\0' : task[0]);
    }
    return out;
}


        int main() {
            auto tc = load_cases("top-k-frequent-elements");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto nums = cases[i]["input"][0].get<std::vector<int>>();
        int k = cases[i]["input"][1].get<int>();
        auto actual = sorted_ints(topKFrequent(nums, k));
        auto expected = cases[i]["expected"].get<std::vector<int>>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), json::Value(expected).to_string(), json::Value(actual).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
