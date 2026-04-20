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
            auto tc = load_cases("mst-kruskal-algo");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) { auto& c = cases[i]; int V = c["input"][0].get<int>(); auto edges = c["input"][1].get<std::vector<std::vector<int>>>(); int actual = kruskalMST(V, edges); int expected = c["expected"].get<int>(); if (actual != expected) report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    report_progress(i + 1, total);
}

            report_ac(total);
        }
