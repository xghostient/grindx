#pragma once

#include <algorithm>
#include <climits>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <variant>
#include <queue>
#include <unordered_set>
#include <vector>

// ===========================================================================
// Minimal JSON parser for grindx test cases (C++17)
// ===========================================================================

namespace json {

struct Value;
using Object = std::map<std::string, Value>;
using Array = std::vector<Value>;
using Null = std::nullptr_t;

struct Value {
    std::variant<Null, bool, long long, double, std::string, Array, Object> data;

    Value() : data(nullptr) {}
    Value(std::nullptr_t) : data(nullptr) {}
    Value(bool b) : data(b) {}
    Value(int n) : data(static_cast<long long>(n)) {}
    Value(long n) : data(static_cast<long long>(n)) {}
    Value(long long n) : data(n) {}
    Value(double d) : data(d) {}
    Value(const std::string& s) : data(s) {}
    Value(const char* s) : data(std::string(s)) {}
    Value(const Array& a) : data(a) {}
    Value(const Object& o) : data(o) {}
    Value(const std::vector<int>& values) : data(Array{}) {
        Array arr;
        arr.reserve(values.size());
        for (int value : values) arr.emplace_back(value);
        data = std::move(arr);
    }
    Value(const std::vector<long long>& values) : data(Array{}) {
        Array arr;
        arr.reserve(values.size());
        for (long long value : values) arr.emplace_back(value);
        data = std::move(arr);
    }
    Value(const std::vector<std::vector<int>>& values) : data(Array{}) {
        Array arr;
        arr.reserve(values.size());
        for (const auto& value : values) arr.emplace_back(value);
        data = std::move(arr);
    }
    Value(const std::vector<std::string>& values) : data(Array{}) {
        Array arr;
        arr.reserve(values.size());
        for (const auto& value : values) arr.emplace_back(value);
        data = std::move(arr);
    }

    bool is_null() const { return std::holds_alternative<Null>(data); }
    bool is_bool() const { return std::holds_alternative<bool>(data); }
    bool is_number() const { return std::holds_alternative<long long>(data) || std::holds_alternative<double>(data); }
    bool is_string() const { return std::holds_alternative<std::string>(data); }
    bool is_array() const { return std::holds_alternative<Array>(data); }
    bool is_object() const { return std::holds_alternative<Object>(data); }

    bool get_bool() const { return std::get<bool>(data); }
    double get_number() const {
        if (std::holds_alternative<long long>(data)) return static_cast<double>(std::get<long long>(data));
        return std::get<double>(data);
    }
    int get_int() const {
        if (std::holds_alternative<long long>(data)) return static_cast<int>(std::get<long long>(data));
        return static_cast<int>(std::get<double>(data));
    }
    long long get_long() const {
        if (std::holds_alternative<long long>(data)) return std::get<long long>(data);
        return static_cast<long long>(std::get<double>(data));
    }
    const std::string& get_string() const { return std::get<std::string>(data); }
    const Array& get_array() const { return std::get<Array>(data); }
    const Object& get_object() const { return std::get<Object>(data); }

    const Value& operator[](size_t i) const { return get_array()[i]; }
    const Value& operator[](const std::string& key) const {
        return get_object().at(key);
    }

    size_t size() const {
        if (is_array()) return get_array().size();
        if (is_object()) return get_object().size();
        return 0;
    }

    template<typename T>
    T get() const;

    std::string to_string() const;
};

// Template specializations for get<T>()
template<> inline int Value::get<int>() const { return get_int(); }
template<> inline double Value::get<double>() const { return get_number(); }
template<> inline long long Value::get<long long>() const { return get_long(); }
template<> inline std::string Value::get<std::string>() const { return get_string(); }
template<> inline bool Value::get<bool>() const { return get_bool(); }

template<> inline std::vector<int> Value::get<std::vector<int>>() const {
    std::vector<int> result;
    for (const auto& v : get_array()) result.push_back(v.get_int());
    return result;
}

template<> inline std::vector<long long> Value::get<std::vector<long long>>() const {
    std::vector<long long> result;
    for (const auto& v : get_array()) result.push_back(v.get_long());
    return result;
}

template<> inline std::vector<std::vector<int>> Value::get<std::vector<std::vector<int>>>() const {
    std::vector<std::vector<int>> result;
    for (const auto& row : get_array()) {
        result.push_back(row.get<std::vector<int>>());
    }
    return result;
}

template<> inline std::vector<std::string> Value::get<std::vector<std::string>>() const {
    std::vector<std::string> result;
    for (const auto& v : get_array()) result.push_back(v.get_string());
    return result;
}

template<> inline std::vector<std::vector<std::string>> Value::get<std::vector<std::vector<std::string>>>() const {
    std::vector<std::vector<std::string>> result;
    for (const auto& row : get_array()) {
        result.push_back(row.get<std::vector<std::string>>());
    }
    return result;
}

template<> inline std::vector<bool> Value::get<std::vector<bool>>() const {
    std::vector<bool> result;
    for (const auto& v : get_array()) result.push_back(v.get_bool());
    return result;
}

inline std::string Value::to_string() const {
    if (is_null()) return "null";
    if (is_bool()) return get_bool() ? "true" : "false";
    if (is_number()) {
        if (std::holds_alternative<long long>(data)) {
            return std::to_string(std::get<long long>(data));
        }
        double d = std::get<double>(data);
        if (d == static_cast<long long>(d))
            return std::to_string(static_cast<long long>(d));
        return std::to_string(d);
    }
    if (is_string()) return "\"" + get_string() + "\"";
    if (is_array()) {
        std::string s = "[";
        for (size_t i = 0; i < get_array().size(); i++) {
            if (i > 0) s += ",";
            s += get_array()[i].to_string();
        }
        return s + "]";
    }
    if (is_object()) {
        std::string s = "{";
        bool first = true;
        for (const auto& [k, v] : get_object()) {
            if (!first) s += ",";
            s += "\"" + k + "\":" + v.to_string();
            first = false;
        }
        return s + "}";
    }
    return "null";
}

// Recursive descent parser
class Parser {
    const std::string& s;
    size_t pos;

    void skip_ws() {
        while (pos < s.size() && std::isspace(s[pos])) pos++;
    }

    std::string parse_string_raw() {
        pos++; // skip "
        std::string result;
        while (pos < s.size()) {
            char c = s[pos];
            if (c == '"') { pos++; return result; }
            if (c == '\\') {
                pos++;
                switch (s[pos]) {
                    case '"': case '\\': case '/': result += s[pos]; break;
                    case 'n': result += '\n'; break;
                    case 't': result += '\t'; break;
                    case 'r': result += '\r'; break;
                    default: result += s[pos];
                }
            } else {
                result += c;
            }
            pos++;
        }
        return result;
    }

    Value parse_value() {
        skip_ws();
        if (pos >= s.size()) return Value();
        char c = s[pos];
        if (c == '"') return Value(parse_string_raw());
        if (c == '{') return parse_object();
        if (c == '[') return parse_array();
        if (c == 't') { pos += 4; return Value(true); }
        if (c == 'f') { pos += 5; return Value(false); }
        if (c == 'n') { pos += 4; return Value(); }
        return parse_number();
    }

    Value parse_number() {
        size_t start = pos;
        if (pos < s.size() && s[pos] == '-') pos++;
        while (pos < s.size() && std::isdigit(s[pos])) pos++;
        bool is_float = false;
        if (pos < s.size() && s[pos] == '.') {
            is_float = true; pos++;
            while (pos < s.size() && std::isdigit(s[pos])) pos++;
        }
        if (pos < s.size() && (s[pos] == 'e' || s[pos] == 'E')) {
            is_float = true; pos++;
            if (pos < s.size() && (s[pos] == '+' || s[pos] == '-')) pos++;
            while (pos < s.size() && std::isdigit(s[pos])) pos++;
        }
        std::string token = s.substr(start, pos - start);
        if (is_float) return Value(std::stod(token));
        return Value(std::stoll(token));
    }

    Value parse_array() {
        pos++; // skip [
        Array arr;
        skip_ws();
        if (pos < s.size() && s[pos] == ']') { pos++; return Value(arr); }
        while (pos < s.size()) {
            arr.push_back(parse_value());
            skip_ws();
            if (pos < s.size() && s[pos] == ',') pos++;
            else break;
        }
        skip_ws();
        if (pos < s.size() && s[pos] == ']') pos++;
        return Value(arr);
    }

    Value parse_object() {
        pos++; // skip {
        Object obj;
        skip_ws();
        if (pos < s.size() && s[pos] == '}') { pos++; return Value(obj); }
        while (pos < s.size()) {
            skip_ws();
            std::string key = parse_string_raw();
            skip_ws();
            pos++; // skip :
            obj[key] = parse_value();
            skip_ws();
            if (pos < s.size() && s[pos] == ',') pos++;
            else break;
        }
        skip_ws();
        if (pos < s.size() && s[pos] == '}') pos++;
        return Value(obj);
    }

public:
    Parser(const std::string& s) : s(s), pos(0) {}
    Value parse() { return parse_value(); }
};

inline Value parse(const std::string& s) {
    Parser p(s);
    return p.parse();
}

} // namespace json

// ===========================================================================
// Data structures (LeetCode standard)
// ===========================================================================

#ifndef GRINDX_LISTNODE_DEFINED
#define GRINDX_LISTNODE_DEFINED
struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* n) : val(x), next(n) {}
};
#endif

#ifndef GRINDX_TREENODE_DEFINED
#define GRINDX_TREENODE_DEFINED
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* l, TreeNode* r) : val(x), left(l), right(r) {}
};
#endif

#ifndef GRINDX_NODE_DEFINED
#define GRINDX_NODE_DEFINED
struct Node {
    int val;
    Node* next;
    Node* random;
    Node* prev;
    Node* child;
    Node* bottom;
    std::vector<Node*> neighbors;
    Node() : val(0), next(nullptr), random(nullptr), prev(nullptr), child(nullptr), bottom(nullptr) {}
    Node(int x) : val(x), next(nullptr), random(nullptr), prev(nullptr), child(nullptr), bottom(nullptr) {}
    Node(int x, std::vector<Node*> n) : val(x), next(nullptr), random(nullptr), prev(nullptr), child(nullptr), bottom(nullptr), neighbors(n) {}
};
#endif

// ===========================================================================
// Serialization / Deserialization
// ===========================================================================

inline ListNode* list_to_linked_list(const json::Array& arr) {
    if (arr.empty()) return nullptr;
    ListNode* head = new ListNode(arr[0].get_int());
    ListNode* curr = head;
    for (size_t i = 1; i < arr.size(); i++) {
        curr->next = new ListNode(arr[i].get_int());
        curr = curr->next;
    }
    return head;
}

inline json::Array linked_list_to_list(ListNode* head) {
    json::Array result;
    std::unordered_set<ListNode*> seen;
    int steps = 0;
    while (head && steps < 100000) {
        if (seen.count(head)) {
            result.push_back(json::Value(INT_MIN));
            return result;
        }
        seen.insert(head);
        result.push_back(json::Value(head->val));
        head = head->next;
        steps++;
    }
    if (head) {
        result.push_back(json::Value(INT_MIN));
    }
    return result;
}

inline TreeNode* list_to_tree(const json::Array& arr) {
    if (arr.empty() || arr[0].is_null()) return nullptr;
    TreeNode* root = new TreeNode(arr[0].get_int());
    std::queue<TreeNode*> q;
    q.push(root);
    size_t i = 1;
    while (!q.empty() && i < arr.size()) {
        TreeNode* node = q.front();
        q.pop();
        if (i < arr.size() && !arr[i].is_null()) {
            node->left = new TreeNode(arr[i].get_int());
            q.push(node->left);
        }
        i++;
        if (i < arr.size() && !arr[i].is_null()) {
            node->right = new TreeNode(arr[i].get_int());
            q.push(node->right);
        }
        i++;
    }
    return root;
}

inline json::Array tree_to_list(TreeNode* root) {
    if (!root) return {};
    json::Array result;
    std::queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();
        if (node == nullptr) {
            result.push_back(json::Value());
        } else {
            result.push_back(json::Value(node->val));
            q.push(node->left);
            q.push(node->right);
        }
    }
    while (!result.empty() && result.back().is_null()) {
        result.pop_back();
    }
    return result;
}

inline Node* adj_list_to_graph(const json::Array& adj_list) {
    if (adj_list.empty()) return nullptr;
    int n = static_cast<int>(adj_list.size());
    std::vector<Node*> nodes(n + 1);
    for (int i = 1; i <= n; i++) nodes[i] = new Node(i);
    for (int i = 0; i < n; i++) {
        for (const auto& nb : adj_list[i].get_array()) {
            nodes[i + 1]->neighbors.push_back(nodes[nb.get_int()]);
        }
    }
    return nodes[1];
}

inline json::Array graph_to_adj_list(Node* node) {
    if (!node) return {};
    std::map<int, Node*> visited;
    std::queue<Node*> q;
    q.push(node);
    visited[node->val] = node;
    while (!q.empty()) {
        Node* n = q.front();
        q.pop();
        for (Node* nb : n->neighbors) {
            if (visited.find(nb->val) == visited.end()) {
                visited[nb->val] = nb;
                q.push(nb);
            }
        }
    }
    int max_val = visited.rbegin()->first;
    json::Array result;
    for (int i = 1; i <= max_val; i++) {
        json::Array neighbors;
        if (visited.count(i)) {
            std::vector<int> vals;
            for (Node* nb : visited[i]->neighbors) vals.push_back(nb->val);
            std::sort(vals.begin(), vals.end());
            for (int v : vals) neighbors.push_back(json::Value(v));
        }
        result.push_back(json::Value(neighbors));
    }
    return result;
}

// ===========================================================================
// Test case loading
// ===========================================================================

inline json::Value load_cases(const std::string& problem_id) {
    std::string path = problem_id + ".json";
    std::ifstream file(path);
    if (!file.is_open()) {
        std::cerr << "Cannot read test cases: " << path << std::endl;
        std::exit(2);
    }
    std::stringstream buf;
    buf << file.rdbuf();
    return json::parse(buf.str());
}

// ===========================================================================
// Comparison
// ===========================================================================

inline bool compare_unordered(std::vector<int> a, std::vector<int> b) {
    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());
    return a == b;
}

inline bool compare_unordered_nested(std::vector<std::vector<int>> a, std::vector<std::vector<int>> b) {
    auto normalize = [](std::vector<std::vector<int>>& values) {
        for (auto& row : values) {
            std::sort(row.begin(), row.end());
        }
        std::sort(values.begin(), values.end());
    };
    normalize(a);
    normalize(b);
    return a == b;
}

inline std::string grindx_vector_to_string(const std::vector<int>& values) {
    json::Array arr;
    for (int value : values) {
        arr.push_back(json::Value(value));
    }
    return json::Value(arr).to_string();
}

inline std::string grindx_matrix_to_string(const std::vector<std::vector<int>>& values) {
    json::Array rows;
    for (const auto& row : values) {
        json::Array arr;
        for (int value : row) {
            arr.push_back(json::Value(value));
        }
        rows.push_back(json::Value(arr));
    }
    return json::Value(rows).to_string();
}

inline std::string grindx_strings_to_string(const std::vector<std::string>& values) {
    json::Array arr;
    for (const auto& value : values) {
        arr.push_back(json::Value(value));
    }
    return json::Value(arr).to_string();
}

inline std::string grindx_bools_to_string(const std::vector<bool>& values) {
    json::Array arr;
    for (bool value : values) {
        arr.push_back(json::Value(value));
    }
    return json::Value(arr).to_string();
}

inline bool compare_exact(const json::Value& actual, const json::Value& expected) {
    return actual.to_string() == expected.to_string();
}

// ===========================================================================
// Verdict reporting
// ===========================================================================

inline std::string truncate(const std::string& s, size_t max_len = 200) {
    if (s.size() <= max_len) return s;
    return s.substr(0, max_len - 3) + "...";
}

inline void report_progress(int passed, int total) {
    const char* path = std::getenv("GRINDX_PROGRESS_FILE");
    if (!path) return;
    static std::fstream out;
    static std::size_t previous_size = 0;
    if (!out.is_open()) {
        out.open(path, std::ios::in | std::ios::out | std::ios::trunc);
        if (!out.is_open()) {
            out.clear();
            out.open(path, std::ios::out | std::ios::trunc);
            out.close();
            out.open(path, std::ios::in | std::ios::out);
        }
    }
    if (!out) return;
    const std::string payload = std::to_string(passed) + "," + std::to_string(total);
    out.seekp(0);
    out.write(payload.c_str(), static_cast<std::streamsize>(payload.size()));
    if (payload.size() < previous_size) {
        const std::string padding(previous_size - payload.size(), ' ');
        out.write(padding.c_str(), static_cast<std::streamsize>(padding.size()));
    }
    out.flush();
    previous_size = payload.size();
}

inline void report_ac(int total) {
    std::cout << "{\"verdict\":\"AC\",\"passed\":" << total
              << ",\"total\":" << total << "}" << std::endl;
    std::exit(0);
}

inline void report_wa(int case_idx, const std::string& input,
                       const std::string& expected, const std::string& actual,
                       int total, const std::string& category = "") {
    auto esc = [](const std::string& s) {
        std::string r;
        for (char c : s) {
            if (c == '"') r += "\\\"";
            else if (c == '\\') r += "\\\\";
            else if (c == '\n') r += "\\n";
            else r += c;
        }
        return r;
    };
    std::cout << "{\"verdict\":\"WA\",\"failed_case\":" << case_idx
              << ",\"input_preview\":\"" << esc(truncate(input))
              << "\",\"expected_preview\":\"" << esc(truncate(expected))
              << "\",\"actual_preview\":\"" << esc(truncate(actual))
              << "\",\"passed\":" << case_idx
              << ",\"total\":" << total
              << ",\"category\":\"" << esc(category) << "\"}" << std::endl;
    std::exit(1);
}
