#include "_common.h"
#include "solution.cpp"

static json::Value build_case(int n, int missing, int repeating) {
    std::vector<int> input(n);
    for (int i = 0; i < n; i++) input[i] = i + 1;
    input[missing - 1] = repeating;

    json::Array wrapped;
    wrapped.reserve(input.size());
    for (int value : input) wrapped.emplace_back(value);
    json::Array input_field;
    input_field.emplace_back(wrapped);
    json::Array expected_field;
    expected_field.emplace_back(repeating);
    expected_field.emplace_back(missing);
    json::Object obj;
    obj["input"] = json::Value(input_field);
    obj["expected"] = json::Value(expected_field);
    obj["category"] = json::Value("stress");
    return json::Value(obj);
}

static std::vector<json::Value> generate_large_cases() {
    const int n = 100000;
    return {
        build_case(n, 1, n),
        build_case(n, n, n / 2),
        build_case(n, 42424, 99999),
    };
}

int main() {
    auto tc = load_cases("missing-repeating");
    auto cases = tc["cases"].get_array();
    auto large_cases = generate_large_cases();
    cases.insert(cases.end(), large_cases.begin(), large_cases.end());
    int total = static_cast<int>(cases.size());

    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        auto expected = c["expected"].get<std::vector<int>>();

                std::vector<int> result = findMissingRepeating(arg0);
                auto actual = result;
        if (actual != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), grindx_vector_to_string(expected), grindx_vector_to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    report_ac(total);
}
