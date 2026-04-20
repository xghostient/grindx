#include "_common.h"
#include "solution.cpp"

static Node* build_bottom(const json::Array& rows) {
    std::vector<Node*> heads;
    for (const auto& row_value : rows) {
        const auto& row = row_value.get_array();
        if (row.empty()) continue;
        Node* head = new Node(row[0].get_int());
        Node* cur = head;
        for (size_t i = 1; i < row.size(); i++) {
            cur->bottom = new Node(row[i].get_int());
            cur = cur->bottom;
        }
        heads.push_back(head);
    }
    for (size_t i = 0; i + 1 < heads.size(); i++) heads[i]->next = heads[i + 1];
    return heads.empty() ? nullptr : heads[0];
}

static json::Array bottom_to_list(Node* head) {
    json::Array out;
    std::unordered_set<Node*> seen;
    while (head) {
        if (seen.count(head)) {
            out.push_back(json::Value(INT_MIN));
            return out;
        }
        seen.insert(head);
        out.push_back(json::Value(head->val));
        head = head->bottom;
    }
    return out;
}

int main() {
    auto tc = load_cases("flatten-dll");
    auto& cases = tc["cases"].get_array();
    int total = static_cast<int>(cases.size());
    for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        json::Array rows = c["input"][0].get_array();
        if (rows.size() == 1 && rows[0].is_array() && rows[0].get_array().empty()) rows = json::Array();
        json::Value actual(bottom_to_list(flatten(build_bottom(rows))));
        json::Value expected(c["expected"].get_array());
        if (actual.to_string() != expected.to_string()) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), expected.to_string(), actual.to_string(), total, cat);
        }
        report_progress(i + 1, total);
    }
    report_ac(total);
}
