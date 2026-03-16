/**
 * Judge for Maximum Depth of Binary Tree — function pattern, tree input, int return.
 */

#include "_common.h"
#include "solution.cpp"

#include <random>

int main() {
    auto tc = load_cases("maximum-depth-of-binary-tree");
    auto& cases = tc["cases"].get_array();

    // Generate large case for TLE detection: a complete binary tree with ~10000 nodes
    struct LargeCase {
        json::Array tree_arr;
        int expected_depth;
    };
    std::vector<LargeCase> large_cases;
    {
        // Build a complete binary tree of depth 14 (2^14 - 1 = 16383 nodes)
        int depth = 14;
        int n = (1 << depth) - 1;
        json::Array arr;
        std::mt19937 rng(42);
        std::uniform_int_distribution<int> dist(-100000, 100000);
        for (int k = 0; k < n; k++) arr.push_back(json::Value(dist(rng)));
        large_cases.push_back({arr, depth});
    }

    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    // Basic cases
    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto& arr = c["input"][0].get_array();
        TreeNode* root = list_to_tree(arr);

        int result = maxDepth(root);
        int expected = c["expected"].get<int>();

        if (result != expected) {
            std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), std::to_string(expected),
                std::to_string(result), total, cat);
        }
    }

    // Large cases
    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        int idx = static_cast<int>(cases.size()) + li;
        auto& lc = large_cases[li];
        TreeNode* root = list_to_tree(lc.tree_arr);

        int result = maxDepth(root);

        if (result != lc.expected_depth) {
            report_wa(idx, "large input (16383 nodes)", std::to_string(lc.expected_depth),
                std::to_string(result), total, "tle");
        }
    }

    report_ac(total);
}
