        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> clone_matrix(const std::vector<std::vector<int>>& matrix) {
    return matrix;
}

static std::vector<std::vector<int>> normalize_pairs(std::vector<std::vector<int>> values) {
    std::sort(values.begin(), values.end());
    return values;
}

static bool graph_shares_identity(Node* original, Node* clone) {
    if (!original || !clone) return false;
    std::set<Node*> original_nodes;
    std::queue<Node*> queue;
    queue.push(original);
    while (!queue.empty()) {
        Node* node = queue.front();
        queue.pop();
        if (!original_nodes.insert(node).second) continue;
        for (Node* neighbor : node->neighbors) queue.push(neighbor);
    }
    std::set<Node*> seen;
    queue.push(clone);
    while (!queue.empty()) {
        Node* node = queue.front();
        queue.pop();
        if (!seen.insert(node).second) continue;
        if (original_nodes.count(node)) return true;
        for (Node* neighbor : node->neighbors) queue.push(neighbor);
    }
    return false;
}


        int main() {
            auto tc = load_cases("surrounded-regions");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        std::vector<std::string> board = c["input"][0].get<std::vector<std::string>>();
        solve(board);
        auto expected = c["expected"].get<std::vector<std::string>>();
        if (board != expected) {
            report_wa(i, c["input"].to_string(), grindx_strings_to_string(expected), grindx_strings_to_string(board), total, c["category"].is_string() ? c["category"].get_string() : "");
        }
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
