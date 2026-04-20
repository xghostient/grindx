        #include "_common.h"
        #include "solution.cpp"

        static std::vector<std::vector<int>> clone_matrix(const std::vector<std::vector<int>>& matrix) {
    return matrix;
}

static bool valid_topological_order(const std::vector<int>& order, int v, const std::vector<std::vector<int>>& adj) {
    if (static_cast<int>(order.size()) != v) return false;
    std::vector<int> pos(v, -1);
    for (int i = 0; i < v; i++) {
        int node = order[i];
        if (node < 0 || node >= v || pos[node] != -1) return false;
        pos[node] = i;
    }
    for (int node = 0; node < v; node++) {
        if (pos[node] == -1) return false;
        for (int nei : adj[node]) {
            if (pos[node] >= pos[nei]) return false;
        }
    }
    return true;
}

static bool valid_course_order(const std::vector<int>& order, int num_courses, const std::vector<std::vector<int>>& prerequisites) {
    if (static_cast<int>(order.size()) != num_courses) return false;
    std::vector<int> pos(num_courses, -1);
    for (int i = 0; i < num_courses; i++) {
        int course = order[i];
        if (course < 0 || course >= num_courses || pos[course] != -1) return false;
        pos[course] = i;
    }
    for (const auto& edge : prerequisites) {
        if (pos[edge[1]] >= pos[edge[0]]) return false;
    }
    return true;
}


        int main() {
            auto tc = load_cases("directed-graph-cycle-dfs");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
            for (int i = 0; i < total; i++) {
        auto& c = cases[i];
        int v = c["input"][0].get<int>();
        std::vector<std::vector<int>> adj = c["input"][1].get<std::vector<std::vector<int>>>();
        bool actual = isCyclic(v, adj);
        bool expected = c["expected"].get_bool();
        if (actual != expected) {
            report_wa(i, c["input"].to_string(), expected ? "true" : "false", actual ? "true" : "false", total, c["category"].is_string() ? c["category"].get_string() : "");
        }
        report_progress(i + 1, total);
    }

            report_ac(total);
        }
