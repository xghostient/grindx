    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("ceil-floor");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto arr = cases[i]["input"][0].get<std::vector<int>>();
    int x = cases[i]["input"][1].get<int>();
    auto result = findFloorCeil(arr, x);
    std::vector<int> actual = {result.first, result.second};
    auto expected = cases[i]["expected"].get<std::vector<int>>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), json::Value(expected).to_string(), json::Value(actual).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
