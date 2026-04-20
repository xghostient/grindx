#include "_common.h"
#include "solution.cpp"

static std::pair<Node*, std::vector<Node*>> build_random(const json::Array& spec) {
    if (spec.empty()) return {nullptr, {}};
    std::vector<Node*> nodes;
    for (const auto& item : spec) nodes.push_back(new Node(item[0].get_int()));
    for (size_t i = 0; i + 1 < nodes.size(); i++) nodes[i]->next = nodes[i + 1];
    for (size_t i = 0; i < nodes.size(); i++) {
        const auto& item = spec[i].get_array();
        if (!item[1].is_null()) nodes[i]->random = nodes[item[1].get_int()];
    }
    return {nodes[0], nodes};
}

static json::Array random_repr(Node* head) {
    std::vector<Node*> nodes;
    std::map<Node*, int> index;
    Node* cur = head;
    while (cur) {
        index[cur] = static_cast<int>(nodes.size());
        nodes.push_back(cur);
        cur = cur->next;
    }
    json::Array out;
    for (auto* node : nodes) {
        json::Array row;
        row.push_back(json::Value(node->val));
        if (!node->random) row.push_back(json::Value());
        else row.push_back(json::Value(index[node->random]));
        out.push_back(json::Value(row));
    }
    return out;
}

static bool contains_node(const std::vector<Node*>& nodes, Node* target) {
    return std::find(nodes.begin(), nodes.end(), target) != nodes.end();
}

int main() {
    auto tc = load_cases("copy-list-with-random-pointer");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        json::Array spec = c["input"][0].get_array();
        if (spec.size() == 1 && spec[0].is_array() && spec[0].get_array().empty()) spec = json::Array();
        auto built = build_random(spec);
        Node* result = copyRandomList(built.first);
        bool deep_ok = true;
        for (Node* cur = result; cur; cur = cur->next) {
            if (contains_node(built.second, cur)) {
                deep_ok = false;
                break;
            }
        }
        json::Value actual(random_repr(result));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string() || !deep_ok) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
