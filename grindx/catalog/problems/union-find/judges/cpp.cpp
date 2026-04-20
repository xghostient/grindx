#include "_common.h"
#include "solution.cpp"

namespace {

struct LargeCase {
    int n;
    std::vector<std::vector<int>> unions;
    std::vector<std::vector<int>> queries;
    std::vector<bool> expected;
};

std::vector<LargeCase> generate_large_cases() {
    std::vector<LargeCase> cases;
    cases.reserve(4);
    for (int variant = 0; variant < 4; variant++) {
        int n = 100000;
        std::vector<std::vector<int>> unions;
        unions.reserve(n - 1);
        for (int i = 0; i < n - 1; i++) unions.push_back({i, i + 1});
        std::vector<std::vector<int>> queries;
        queries.reserve(100000);
        if (variant == 0) {
            for (int i = 0; i < 100000; i++) queries.push_back({0, n - 1});
        } else if (variant == 1) {
            for (int i = 0; i < 100000; i++) queries.push_back({0, n - 1 - i});
        } else if (variant == 2) {
            for (int i = 0; i < 100000; i++) queries.push_back({i, n - 1});
        } else {
            for (int i = 0; i < 50000; i++) {
                queries.push_back({0, n / 2});
                queries.push_back({n / 3, n - 1});
            }
        }
        cases.push_back({n, unions, queries, std::vector<bool>(queries.size(), true)});
    }
    return cases;
}

}  // namespace

int main() {
    auto tc = load_cases("union-find");
    auto& cases = tc["cases"].get_array();
    auto large_cases = generate_large_cases();
    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        int n = c["input"][0].get<int>();
        auto unions = c["input"][1].get<std::vector<std::vector<int>>>();
        auto queries = c["input"][2].get<std::vector<std::vector<int>>>();
        auto expected = c["expected"].get<std::vector<bool>>();
        UnionFind uf(n);
        for (const auto& pair : unions) {
            uf.Union(pair[0], pair[1]);
        }
        std::vector<bool> actual;
        for (const auto& pair : queries) {
            actual.push_back(uf.Connected(pair[0], pair[1]));
        }
        if (actual != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), grindx_bools_to_string(expected), grindx_bools_to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        const auto& c = large_cases[li];
        UnionFind uf(c.n);
        for (const auto& pair : c.unions) {
            uf.Union(pair[0], pair[1]);
        }
        std::vector<bool> actual;
        actual.reserve(c.queries.size());
        for (const auto& pair : c.queries) {
            actual.push_back(uf.Connected(pair[0], pair[1]));
        }
        if (actual != c.expected) {
            report_wa(
                static_cast<int>(cases.size()) + li,
                "large input",
                grindx_bools_to_string(c.expected),
                grindx_bools_to_string(actual),
                total,
                "tle"
            );
        }
    }

    report_ac(total);
}
