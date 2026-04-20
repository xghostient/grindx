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
            auto tc = load_cases("task-scheduler");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto tasks = cases[i]["input"][0].get<std::vector<std::string>>();
        int n = cases[i]["input"][1].get<int>();
        std::string taskString = tasks_to_string(tasks);
        int actual = leastInterval(taskString, n);
        int expected = cases[i]["expected"].get<int>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
