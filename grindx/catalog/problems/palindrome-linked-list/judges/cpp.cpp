#include "_common.h"
#include "solution.cpp"

int main() {
    auto tc = load_cases("palindrome-linked-list");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        bool actual = isPalindrome(list_to_linked_list(c["input"][0].get_array()));
        bool expected = c["expected"].get_bool();
        if (actual != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
