#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("disjoint-set-implementation");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        int n = c["input"][0].get<int>();
        DSU dsu(n);
        auto ops = c["operations"].get<std::vector<std::string>>();
        auto& inputs = c["op_inputs"].get_array();
        auto& expected = c["expected"].get_array();
        for (size_t j = 0; j < ops.size(); j++) {
            auto args = inputs[j].get<std::vector<int>>();
            bool actual = ops[j] == "union" ? dsu.Union(args[0], args[1]) : dsu.Find(args[0]) == dsu.Find(args[1]);
            bool want = expected[j].get_bool();
            if (actual != want) {
                report_wa(i, c["input"].to_string(), want ? "true" : "false", actual ? "true" : "false", total, c["category"].is_string() ? c["category"].get_string() : "");
            }
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
