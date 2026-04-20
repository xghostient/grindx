    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("unique-paths");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    int m = c["input"][0].get<int>();
    int n = c["input"][1].get<int>();
    int actual = uniquePaths(m, n);
    int expected = c["expected"].get<int>();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
