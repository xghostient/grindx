        #include "_common.h"
        #include "solution.cpp"

        std::string vector_to_string(const std::vector<int>& values) {
    json::Array arr;
    for (int value : values) {
        arr.push_back(json::Value(value));
    }
    return json::Value(arr).to_string();
}

        int main() {
            auto tc = load_cases("product-of-array-except-self");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());

            for (int i = 0; i < total; i++) {
                auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        auto expected = c["expected"].get<std::vector<int>>();

        std::vector<int> result = productExceptSelf(arg0);

        if (result != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), vector_to_string(expected), vector_to_string(result), total, category);
        }
                report_progress(i + 1, total);
    }

    report_ac(total);
}
