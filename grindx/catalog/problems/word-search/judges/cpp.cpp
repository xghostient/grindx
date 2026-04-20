    #include "_common.h"
    #include "solution.cpp"



    int main() {
        auto tc = load_cases("word-search");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto rawBoard = cases[i]["input"][0].get<std::vector<std::vector<std::string>>>();
    std::vector<std::string> board;
    for (const auto& row : rawBoard) {
        std::string s;
        for (const auto& ch : row) s += ch;
        board.push_back(s);
    }
    auto word = cases[i]["input"][1].get<std::string>();
    bool actual = exist(board, word);
    bool expected = cases[i]["expected"].get<bool>();
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
