        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::string> get_string_array(const json::Value& value) {
    std::vector<std::string> out;
    for (const auto& item : value.get_array()) out.push_back(item.get_string());
    return out;
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

static std::vector<std::vector<std::string>> normalize_string_groups(std::vector<std::vector<std::string>> groups) {
    for (auto& row : groups) std::sort(row.begin(), row.end());
    std::sort(groups.begin(), groups.end());
    return groups;
}

static std::vector<std::string> derive_probe_strings(std::vector<std::string> strs) {
    for (auto& value : strs) value += "#probe";
    strs.push_back("|probe|");
    return strs;
}

static std::string string_matrix_to_string(const std::vector<std::vector<std::string>>& matrix) {
    json::Array rows;
    for (const auto& row : matrix) {
        json::Array arr;
        for (const auto& value : row) arr.push_back(json::Value(value));
        rows.push_back(json::Value(arr));
    }
    return json::Value(rows).to_string();
}

        static bool is_valid_longest_palindrome(const std::string& source, const std::string& expected, const std::string& actual) {
    if (actual.size() != expected.size()) return false;
    if (source.find(actual) == std::string::npos) return false;
    return std::equal(actual.begin(), actual.begin() + actual.size() / 2, actual.rbegin());
}

static bool is_valid_frequency_sort(const std::string& source, const std::string& actual) {
    if (source.size() != actual.size()) return false;
    std::unordered_map<char, int> counts;
    std::unordered_map<char, int> seen;
    for (char ch : source) counts[ch]++;
    for (char ch : actual) seen[ch]++;
    if (counts != seen) return false;
    for (size_t i = 1; i < actual.size(); ++i) {
        if (counts[actual[i - 1]] < counts[actual[i]]) return false;
    }
    return true;
}


        int main() {
            auto tc = load_cases("max-score-from-removing-substr");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    std::string s = c["input"][0].get_string();
    int x = c["input"][1].get_int();
    int y = c["input"][2].get_int();
    int actual = maximumGain(s, x, y);
    int expected = c["expected"].get_int();
    if (actual != expected) {
        report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

            report_ac(total);
        }
