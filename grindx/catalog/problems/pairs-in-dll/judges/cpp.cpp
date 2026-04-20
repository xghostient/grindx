#include "_common.h"
#include "solution.cpp"

static DLLNode* list_to_dll(const json::Array& arr) {
    if (arr.empty()) return nullptr;
    DLLNode* head = new DLLNode(arr[0].get_int());
    DLLNode* cur = head;
    for (size_t i = 1; i < arr.size(); i++) {
        DLLNode* node = new DLLNode(arr[i].get_int());
        node->prev = cur;
        cur->next = node;
        cur = node;
    }
    return head;
}

static json::Array normalize_pairs(const std::vector<std::vector<int>>& result) {
    std::vector<std::vector<int>> pairs = result;
    std::sort(pairs.begin(), pairs.end());
    json::Array out;
    for (const auto& pair : pairs) {
        json::Array row;
        row.push_back(json::Value(pair[0]));
        row.push_back(json::Value(pair[1]));
        out.push_back(json::Value(row));
    }
    return out;
}

int main() {
    auto tc = load_cases("pairs-in-dll");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto actual = json::Value(normalize_pairs(findPairs(list_to_dll(c["input"][0].get_array()), c["input"][1].get<int>())));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
