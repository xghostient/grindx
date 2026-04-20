#include "_common.h"
#include "solution.cpp"

static json::Value build_case(const std::vector<int>& input, const std::vector<int>& expected) {
    json::Array wrapped;
    wrapped.reserve(input.size());
    for (int value : input) wrapped.emplace_back(value);
    json::Array input_field;
    input_field.emplace_back(wrapped);
    json::Array expected_field;
    expected_field.reserve(expected.size());
    for (int value : expected) expected_field.emplace_back(value);
    json::Object obj;
    obj["input"] = json::Value(input_field);
    obj["expected"] = json::Value(expected_field);
    obj["category"] = json::Value("stress");
    return json::Value(obj);
}

static std::vector<json::Value> generate_large_cases() {
    std::vector<json::Value> out;
    std::vector<int> stress_one(50000);
    for (int i = 0; i < 16666; i++) stress_one[i] = i + 3;
    for (int i = 16666; i < 33333; i++) stress_one[i] = 1;
    for (int i = 33333; i < 50000; i++) stress_one[i] = 2;
    out.push_back(build_case(stress_one, {1, 2}));

    std::vector<int> stress_two(50000);
    for (int i = 0; i < 33333; i++) stress_two[i] = i + 2;
    for (int i = 33333; i < 50000; i++) stress_two[i] = 1;
    out.push_back(build_case(stress_two, {1}));

    std::vector<int> stress_three(50000);
    for (int i = 0; i < 16666; i++) stress_three[i] = -(i + 3);
    for (int i = 16666; i < 33333; i++) stress_three[i] = -1;
    for (int i = 33333; i < 50000; i++) stress_three[i] = -2;
    out.push_back(build_case(stress_three, {-2, -1}));

    std::vector<int> stress_four(50000);
    for (int i = 0; i < 33333; i++) stress_four[i] = 1000000000 - i;
    for (int i = 33333; i < 50000; i++) stress_four[i] = 999999999;
    out.push_back(build_case(stress_four, {999999999}));

    std::vector<int> stress_five(50000);
    for (int i = 0; i < 16666; i++) stress_five[i] = 500000000 + i;
    for (int i = 16666; i < 33333; i++) stress_five[i] = 7;
    for (int i = 33333; i < 50000; i++) stress_five[i] = 8;
    out.push_back(build_case(stress_five, {7, 8}));

    std::vector<int> stress_six(50000);
    for (int i = 0; i < 33333; i++) stress_six[i] = -(500000000 + i);
    for (int i = 33333; i < 50000; i++) stress_six[i] = -7;
    out.push_back(build_case(stress_six, {-7}));

    std::vector<int> stress_seven(50000);
    for (int i = 0; i < 16666; i++) stress_seven[i] = 250000000 + i;
    for (int i = 16666; i < 33333; i++) stress_seven[i] = 123456789;
    for (int i = 33333; i < 50000; i++) stress_seven[i] = 987654321;
    out.push_back(build_case(stress_seven, {123456789, 987654321}));

    std::vector<int> stress_eight(50000);
    for (int i = 0; i < 33333; i++) stress_eight[i] = -(250000000 + i);
    for (int i = 33333; i < 50000; i++) stress_eight[i] = -123456789;
    out.push_back(build_case(stress_eight, {-123456789}));
    auto base = out;
    for (int rep = 1; rep < 4; rep++) {
        out.insert(out.end(), base.begin(), base.end());
    }
    return out;
}

int main() {
    auto tc = load_cases("majority-element-2");
    auto cases = tc["cases"].get_array();
    auto large_cases = generate_large_cases();
    cases.insert(cases.end(), large_cases.begin(), large_cases.end());
    int total = static_cast<int>(cases.size());

    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        auto expected = c["expected"].get<std::vector<int>>();

                std::vector<int> result = majorityElement(arg0);
                auto actual = result;
        if (!compare_unordered(actual, expected)) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), grindx_vector_to_string(expected), grindx_vector_to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    report_ac(total);
}
