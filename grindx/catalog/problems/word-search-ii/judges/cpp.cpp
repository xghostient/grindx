    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("word-search-ii");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto rawBoard = cases[i]["input"][0].get<std::vector<std::vector<std::string>>>();
    std::vector<std::string> board;
    for (auto& row : rawBoard) {
        std::string s;
        for (auto& ch : row) s += ch.empty() ? '\0' : ch[0];
        board.push_back(s);
    }
    auto words = cases[i]["input"][1].get<std::vector<std::string>>();
    auto result = findWords(board, words);
    std::sort(result.begin(), result.end());
    auto expected = cases[i]["expected"].get<std::vector<std::string>>();
    std::sort(expected.begin(), expected.end());
    if (result != expected) report_wa(i, cases[i]["input"].to_string(), json::Value(expected).to_string(), json::Value(result).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}

        report_ac(total);
    }
