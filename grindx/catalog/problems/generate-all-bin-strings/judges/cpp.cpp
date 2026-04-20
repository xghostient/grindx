        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::string> normalize_str_list(std::vector<std::string> values) {
    std::sort(values.begin(), values.end());
    return values;
}

static std::string str_list_to_string(const std::vector<std::string>& items) {
    json::Array arr;
    for (const auto& s : items) arr.push_back(json::Value(s));
    return json::Value(arr).to_string();
}


        int main() {
            auto tc = load_cases("generate-all-bin-strings");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        int n = cases[i]["input"][0].get<int>();
        auto actual = normalize_str_list(generateBinaryStrings(n));
        auto expected = cases[i]["expected"].get<std::vector<std::string>>();
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), str_list_to_string(expected), str_list_to_string(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
