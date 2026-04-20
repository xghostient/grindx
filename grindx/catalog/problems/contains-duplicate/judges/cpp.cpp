#include "_common.h"
#include "solution.cpp"


int main() {
    auto tc = load_cases("contains-duplicate");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());

    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        bool expected = c["expected"].get_bool();

        bool result = containsDuplicate(arg0);

        if (result != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), std::string(expected ? "true" : "false"), std::string(result ? "true" : "false"), total, category);
        }
        report_progress(i + 1, total);
    }

    report_ac(total);
}
