        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<std::string>> get_string_matrix(const json::Value& value) {
    std::vector<std::vector<std::string>> out;
    for (const auto& row_value : value.get_array()) {
        std::vector<std::string> row;
        for (const auto& cell : row_value.get_array()) row.push_back(cell.get_string());
        out.push_back(row);
    }
    return out;
}

static std::vector<std::vector<std::string>> normalize_paths(std::vector<std::vector<std::string>> paths) {
    std::sort(paths.begin(), paths.end());
    return paths;
}

static std::string string_matrix_to_string(const std::vector<std::vector<std::string>>& matrix) {
    std::string out = "[";
    for (size_t i = 0; i < matrix.size(); i++) {
        if (i > 0) out += ",";
        out += "[";
        for (size_t j = 0; j < matrix[i].size(); j++) {
            if (j > 0) out += ",";
            out += """ + matrix[i][j] + """;
        }
        out += "]";
    }
    out += "]";
    return out;
}

static bool validate_alien_order(const std::vector<std::string>& words, const std::string& order) {
    std::unordered_set<char> chars;
    for (const auto& word : words) for (char ch : word) chars.insert(ch);
    if (order.size() != chars.size()) return false;
    std::unordered_map<char, int> rank;
    for (int i = 0; i < static_cast<int>(order.size()); i++) {
        if (rank.count(order[i])) return false;
        rank[order[i]] = i;
    }
    for (char ch : chars) if (!rank.count(ch)) return false;
    for (size_t i = 0; i + 1 < words.size(); i++) {
        const auto& a = words[i];
        const auto& b = words[i + 1];
        size_t j = 0;
        while (j < a.size() && j < b.size() && a[j] == b[j]) j++;
        if (j == std::min(a.size(), b.size())) {
            if (a.size() > b.size()) return false;
            continue;
        }
        if (rank[a[j]] > rank[b[j]]) return false;
    }
    return true;
}


        int main() {
            auto tc = load_cases("word-ladder");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        std::string beginWord = c["input"][0].get<std::string>();
        std::string endWord = c["input"][1].get<std::string>();
        auto wordList = c["input"][2].get<std::vector<std::string>>();
        int actual = ladderLength(beginWord, endWord, wordList);
        int expected = c["expected"].get<int>();
        if (actual != expected) {
            report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
        }
                report_progress(i + 1, total);
    }

            report_ac(total);
        }
