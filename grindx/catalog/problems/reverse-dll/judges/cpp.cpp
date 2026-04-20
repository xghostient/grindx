#include "_common.h"
#include "solution.cpp"

static std::pair<DLLNode*, std::vector<DLLNode*>> list_to_dll(const json::Array& arr) {
    if (arr.empty()) return {nullptr, {}};
    DLLNode* head = new DLLNode(arr[0].get_int());
    std::vector<DLLNode*> nodes{head};
    DLLNode* cur = head;
    for (size_t i = 1; i < arr.size(); i++) {
        DLLNode* node = new DLLNode(arr[i].get_int());
        node->prev = cur;
        cur->next = node;
        cur = node;
        nodes.push_back(node);
    }
    return {head, nodes};
}

static json::Array dll_to_list(DLLNode* head) {
    json::Array out;
    std::unordered_set<DLLNode*> seen;
    DLLNode* prev = nullptr;
    while (head) {
        if (seen.count(head) || head->prev != prev) {
            out.push_back(json::Value(INT_MIN));
            return out;
        }
        seen.insert(head);
        out.push_back(json::Value(head->val));
        prev = head;
        head = head->next;
    }
    return out;
}

int main() {
    auto tc = load_cases("reverse-dll");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        auto built = list_to_dll(c["input"][0].get_array());
        DLLNode* head = built.first;
        auto nodes = built.second;
        json::Value actual(dll_to_list(reverseDLL(head)));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
