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
            auto tc = load_cases("clone-graph");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        Node* graph = adj_list_to_graph(c["input"][0].get_array());
        Node* cloned = cloneGraph(graph);
        if (graph_shares_identity(graph, cloned)) {
            report_wa(i, c["input"].to_string(), std::string("deep copy without shared nodes"), std::string("shared original nodes"), total, c["category"].is_string() ? c["category"].get_string() : "");
        }
        auto actual = graph_to_adj_list(cloned);
        auto actual_value = json::Value(actual);
        auto expected = c["expected"].to_string();
        if (actual_value.to_string() != expected) {
            report_wa(i, c["input"].to_string(), expected, actual_value.to_string(), total, c["category"].is_string() ? c["category"].get_string() : "");
        }
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
