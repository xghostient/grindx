    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("jump-game");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    auto nums = c["input"][0].get<std::vector<int>>();
    bool actual = canJump(nums);
    bool expected = c["expected"].get<bool>();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, c["category"].is_string() ? c["category"].get_string() : "");
    }
            report_progress(i + 1, total);
}

        report_ac(total);
    }
