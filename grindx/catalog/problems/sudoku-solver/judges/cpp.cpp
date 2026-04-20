    #include "_common.h"
    #include "solution.cpp"



    int main() {
        auto tc = load_cases("sudoku-solver");
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
    solveSudoku(board);
    auto rawExpected = cases[i]["expected"].get<std::vector<std::vector<std::string>>>();
    std::vector<std::string> expected;
    for (const auto& row : rawExpected) {
        std::string s;
        for (const auto& ch : row) s += ch;
        expected.push_back(s);
    }
    if (board != expected) {
        json::Array actual_arr;
        for (const auto& row : board) actual_arr.push_back(json::Value(row));
        report_wa(i, cases[i]["input"].to_string(), cases[i]["expected"].to_string(), json::Value(actual_arr).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

        report_ac(total);
    }
