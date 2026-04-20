        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> clone_matrix(const std::vector<std::vector<int>>& matrix) {
    return matrix;
}

static std::vector<std::vector<std::string>> get_string_matrix(const json::Value& value) {
    std::vector<std::vector<std::string>> out;
    for (const auto& row_value : value.get_array()) {
        std::vector<std::string> row;
        for (const auto& cell : row_value.get_array()) row.push_back(cell.get_string());
        out.push_back(row);
    }
    return out;
}

static std::vector<std::vector<std::string>> normalize_accounts(std::vector<std::vector<std::string>> accounts) {
    for (auto& account : accounts) {
        if (account.empty()) continue;
        std::vector<std::string> emails(account.begin() + 1, account.end());
        std::sort(emails.begin(), emails.end());
        emails.erase(std::unique(emails.begin(), emails.end()), emails.end());
        account.erase(account.begin() + 1, account.end());
        account.insert(account.end(), emails.begin(), emails.end());
    }
    std::sort(accounts.begin(), accounts.end());
    return accounts;
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


        int main() {
            auto tc = load_cases("make-a-large-island");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto grid = c["input"][0].get<std::vector<std::vector<int>>>();
        int actual = largestIsland(grid);
        int expected = c["expected"].get<int>();
        if (actual != expected) {
            report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
        }
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
