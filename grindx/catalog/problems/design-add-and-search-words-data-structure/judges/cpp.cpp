#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("design-add-and-search-words-data-structure");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        WordDictionary obj;
        auto ops = c["operations"].get<std::vector<std::string>>();
        auto& inputs = c["op_inputs"].get_array();
        auto& expected = c["expected"].get_array();
        for (size_t j = 0; j < ops.size(); j++) {
            std::string op = ops[j];
            auto strArgs = inputs[j].get<std::vector<std::string>>();
            json::Value actual;
                            if (op == "addWord") {
                                obj.AddWord(strArgs[0]); actual = json::Value();
                            }
                            if (op == "search") {
                                actual = json::Value(obj.Search(strArgs[0]));
                            }
            if (actual.to_string() != expected[j].to_string()) {
                report_wa(i, c["input"].to_string(), expected[j].to_string(), actual.to_string(), total, c["category"].is_string() ? c["category"].get_string() : "");
            }
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
