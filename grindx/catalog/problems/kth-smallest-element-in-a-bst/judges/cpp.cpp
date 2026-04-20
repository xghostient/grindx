        #include "_common.h"
        #include "solution.cpp"

        static TreeNode* find_node(TreeNode* root, int target) {
    if (!root) return nullptr;
    if (root->val == target) return root;
    TreeNode* left = find_node(root->left, target);
    if (left) return left;
    return find_node(root->right, target);
}

static std::vector<int> inorder_values(TreeNode* root) {
    if (!root) return {};
    auto out = inorder_values(root->left);
    out.push_back(root->val);
    auto right = inorder_values(root->right);
    out.insert(out.end(), right.begin(), right.end());
    return out;
}

static std::vector<int> preorder_values(TreeNode* root) {
    if (!root) return {};
    std::vector<int> out{root->val};
    auto left = preorder_values(root->left);
    auto right = preorder_values(root->right);
    out.insert(out.end(), left.begin(), left.end());
    out.insert(out.end(), right.begin(), right.end());
    return out;
}

static std::vector<int> postorder_values(TreeNode* root) {
    if (!root) return {};
    auto out = postorder_values(root->left);
    auto right = postorder_values(root->right);
    out.insert(out.end(), right.begin(), right.end());
    out.push_back(root->val);
    return out;
}

static std::vector<std::vector<int>> level_order_values(TreeNode* root) {
    if (!root) return {};
    std::vector<std::vector<int>> out;
    std::queue<std::pair<TreeNode*, int>> q;
    q.push({root, 0});
    while (!q.empty()) {
        auto [node, depth] = q.front();
        q.pop();
        if (depth == static_cast<int>(out.size())) out.push_back({});
        out[depth].push_back(node->val);
        if (node->left) q.push({node->left, depth + 1});
        if (node->right) q.push({node->right, depth + 1});
    }
    return out;
}

static bool is_balanced_tree(TreeNode* root) {
    std::function<std::pair<int, bool>(TreeNode*)> height = [&](TreeNode* node) {
        if (!node) return std::pair<int, bool>{0, true};
        auto [lh, lok] = height(node->left);
        auto [rh, rok] = height(node->right);
        if (!lok || !rok || std::abs(lh - rh) > 1) return std::pair<int, bool>{0, false};
        return std::pair<int, bool>{1 + std::max(lh, rh), true};
    };
    return height(root).second;
}


        int main() {
            auto tc = load_cases("kth-smallest-element-in-a-bst");
            auto& cases = tc["cases"].get_array();
            int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto& c = cases[i];
    int actual = kthSmallest(list_to_tree(c["input"][0].get_array()), c["input"][1].get<int>());
    int expected = c["expected"].get<int>();
    if (actual != expected) {
        std::string cat = c["category"].is_string() ? c["category"].get_string() : "";
        report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, cat);
    }
            report_progress(i + 1, total);
}

            report_ac(total);
        }
