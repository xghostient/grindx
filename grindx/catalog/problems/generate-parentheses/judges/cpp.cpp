        #include "_common.h"
        #include "solution.cpp"

        static std::string string_vector_json(std::vector<std::string> values) {
    json::Array arr;
    for (const auto& value : values) arr.emplace_back(value);
    return json::Value(arr).to_string();
}


        int main() {
            auto tc = load_cases("generate-parentheses");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        int n = cases[i]["input"][0].get<int>();
        auto actual = generateParenthesis(n);
        auto expected = cases[i]["expected"].get<std::vector<std::string>>();
        std::sort(actual.begin(), actual.end());
        std::sort(expected.begin(), expected.end());
        if (actual != expected) report_wa(i, cases[i]["input"].to_string(), string_vector_json(expected), string_vector_json(actual), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
