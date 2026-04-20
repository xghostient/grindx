#include "_common.h"
#include "solution.cpp"

static Node* build_level(const json::Array& spec) {
    if (spec.empty()) return nullptr;
    Node* head = nullptr;
    Node* prev = nullptr;
    for (const auto& item_value : spec) {
        const auto& item = item_value.get_object();
        Node* node = new Node(item.at("val").get_int());
        if (!head) head = node;
        if (prev) {
            prev->next = node;
            node->prev = prev;
        }
        auto it = item.find("child");
        if (it != item.end() && it->second.is_array() && !it->second.get_array().empty()) {
            node->child = build_level(it->second.get_array());
        }
        prev = node;
    }
    return head;
}

static json::Array multi_to_list(Node* head) {
    json::Array out;
    std::unordered_set<Node*> seen;
    Node* prev = nullptr;
    while (head) {
        if (seen.count(head) || head->prev != prev || head->child != nullptr) {
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
    auto tc = load_cases("flatten-a-multilevel-doubly-linked-list");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        json::Value actual(multi_to_list(flatten(build_level(c["input"][0].get_array()))));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
