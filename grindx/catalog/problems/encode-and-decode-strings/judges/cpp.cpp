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


        int main() {
            auto tc = load_cases("encode-and-decode-strings");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    auto strs = get_string_array(c["input"][0]);
    auto expected = get_string_array(c["expected"]);
    auto encoded = encode(strs);
    auto encoded_copy = encoded;
    auto actual = decode(encoded_copy);
    auto probe = derive_probe_strings(strs);
    auto probe_encoded = encode(probe);
    (void)probe_encoded;
    auto encoded_again = encoded;
    auto roundtrip = decode(encoded_again);
    if (actual != expected || roundtrip != expected) {
        report_wa(i, c["input"].to_string(), grindx_strings_to_string(expected), grindx_strings_to_string(actual), total, c["category"].is_string() ? c["category"].get_string() : "");
    }
    report_progress(i + 1, total);
}

            report_ac(total);
        }
