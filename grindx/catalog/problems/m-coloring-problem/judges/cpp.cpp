    #include "_common.h"
    #include "solution.cpp"



    int main() {
        auto tc = load_cases("m-coloring-problem");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    int n = cases[i]["input"][0].get<int>();
    auto rawEdges = cases[i]["input"][1].get<std::vector<std::vector<int>>>();
    int m = cases[i]["input"][2].get<int>();
    bool actual = graphColoring(n, rawEdges, m);
    bool expected = cases[i]["expected"].get<bool>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
