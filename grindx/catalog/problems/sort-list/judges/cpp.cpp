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

    std::vector<int> descending(50000);
    std::vector<int> descending_expected(50000);
    for (int i = 0; i < 50000; i++) {
        descending[i] = 50000 - i;
        descending_expected[i] = i + 1;
    }
    out.push_back(build_case(descending, descending_expected));

    std::vector<int> mixed(50000);
    for (int i = 0; i < 50000; i++) {
        mixed[i] = ((i * 8191) % 200001) - 100000;
    }
    std::vector<int> mixed_expected = mixed;
    std::sort(mixed_expected.begin(), mixed_expected.end());
    out.push_back(build_case(mixed, mixed_expected));

    std::vector<int> duplicates(50000);
    for (int i = 0; i < 50000; i++) {
        duplicates[i] = ((i * 37) % 31) - 15;
    }
    std::vector<int> duplicates_expected = duplicates;
    std::sort(duplicates_expected.begin(), duplicates_expected.end());
    out.push_back(build_case(duplicates, duplicates_expected));

    return out;
}

int main() {
    auto tc = load_cases("sort-list");
    auto cases = tc["cases"].get_array();
    auto large_cases = generate_large_cases();
    cases.insert(cases.end(), large_cases.begin(), large_cases.end());
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        ListNode* head = list_to_linked_list(c["input"][0].get_array());
        json::Value actual(linked_list_to_list(sortList(head)));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
