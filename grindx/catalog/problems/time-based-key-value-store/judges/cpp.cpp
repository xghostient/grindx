#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("time-based-key-value-store");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        TimeMap obj;
        auto ops = c["operations"].get<std::vector<std::string>>();
        auto& inputs = c["op_inputs"].get_array();
        auto& expected = c["expected"].get_array();
        for (size_t j = 0; j < ops.size(); j++) {
            std::string op = ops[j];
            json::Value actual;
            if (op == "TimeMap") {
                actual = json::Value();
            } else if (op == "set") {
                std::string key = inputs[j][0].get<std::string>();
                std::string value = inputs[j][1].get<std::string>();
                int ts = inputs[j][2].get<int>();
                obj.Set(key, value, ts);
                actual = json::Value();
            } else if (op == "get") {
                std::string key = inputs[j][0].get<std::string>();
                int ts = inputs[j][1].get<int>();
                actual = json::Value(obj.Get(key, ts));
            }
            if (actual.to_string() != expected[j].to_string()) {
                report_wa(i, c["input"].to_string(), expected[j].to_string(), actual.to_string(), total, c["category"].is_string() ? c["category"].get_string() : "");
            }
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
