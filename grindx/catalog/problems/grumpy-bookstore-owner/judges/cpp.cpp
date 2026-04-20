#include "_common.h"
#include "solution.cpp"

namespace {

struct LargeCase {
    std::vector<int> customers;
    std::vector<int> grumpy;
    int minutes;
    int expected;
};

int expected(const std::vector<int>& customers, const std::vector<int>& grumpy, int minutes) {
    int base = 0;
    for (int i = 0; i < static_cast<int>(customers.size()); i++) {
        if (grumpy[i] == 0) base += customers[i];
    }
    int extra = 0;
    for (int i = 0; i < minutes; i++) {
        if (grumpy[i] == 1) extra += customers[i];
    }
    int best = extra;
    for (int i = minutes; i < static_cast<int>(customers.size()); i++) {
        if (grumpy[i] == 1) extra += customers[i];
        if (grumpy[i - minutes] == 1) extra -= customers[i - minutes];
        if (extra > best) best = extra;
    }
    return base + best;
}

std::vector<LargeCase> generate_large_cases() {
    int n = 20000;
    std::vector<LargeCase> cases;
    cases.reserve(32);
    for (int shift = 0; shift < 8; shift++) {
        std::vector<int> customers(n), grumpy(n, 1);
        for (int i = 0; i < n; i++) customers[i] = (i + shift) % 2 == 0 ? 1000 : 1;
        int minutes = n / 2 + (shift % 5);
        cases.push_back({customers, grumpy, minutes, expected(customers, grumpy, minutes)});
    }
    for (int shift = 0; shift < 8; shift++) {
        std::vector<int> customers(n), grumpy(n);
        for (int i = 0; i < n; i++) {
            customers[i] = ((i + shift) % 9) * 111;
            grumpy[i] = (i + shift) % 3 == 0 ? 1 : 0;
        }
        int minutes = n / 2 + (shift % 7);
        cases.push_back({customers, grumpy, minutes, expected(customers, grumpy, minutes)});
    }
    for (int shift = 0; shift < 8; shift++) {
        std::vector<int> customers(n), grumpy(n);
        for (int i = 0; i < n; i++) {
            customers[i] = (i + shift) % 4 < 2 ? 5 : 20;
            grumpy[i] = (i + shift) % 5 != 0 ? 1 : 0;
        }
        int minutes = n / 3 + (shift % 11);
        cases.push_back({customers, grumpy, minutes, expected(customers, grumpy, minutes)});
    }
    for (int shift = 0; shift < 8; shift++) {
        std::vector<int> customers(n), grumpy(n);
        for (int i = 0; i < n; i++) {
            customers[i] = 997 - ((i + shift) % 11);
            grumpy[i] = (i + shift) % 2 == 0 ? 1 : 0;
        }
        int minutes = n - 123 - (shift % 17);
        cases.push_back({customers, grumpy, minutes, expected(customers, grumpy, minutes)});
    }
    return cases;
}

}  // namespace

int main() {
    auto tc = load_cases("grumpy-bookstore-owner");
    auto& cases = tc["cases"].get_array();
    auto large_cases = generate_large_cases();
    int total = static_cast<int>(cases.size()) + static_cast<int>(large_cases.size());

    for (int i = 0; i < static_cast<int>(cases.size()); i++) {
        auto& c = cases[i];
        auto arg0 = c["input"][0].get<std::vector<int>>();
        auto arg1 = c["input"][1].get<std::vector<int>>();
        int arg2 = c["input"][2].get<int>();
        int expected = c["expected"].get<int>();

                int result = maxSatisfied(arg0, arg1, arg2);
                auto actual = result;
        if (actual != expected) {
            std::string category = c["category"].is_string() ? c["category"].get_string() : "";
            report_wa(i, c["input"].to_string(), std::to_string(expected), std::to_string(actual), total, category);
        }
        report_progress(i + 1, total);
    }

    for (int li = 0; li < static_cast<int>(large_cases.size()); li++) {
        auto customers = large_cases[li].customers;
        auto grumpy = large_cases[li].grumpy;
        int actual = maxSatisfied(customers, grumpy, large_cases[li].minutes);
        if (actual != large_cases[li].expected) {
            report_wa(
                static_cast<int>(cases.size()) + li,
                "large input",
                std::to_string(large_cases[li].expected),
                std::to_string(actual),
                total,
                "tle"
            );
        }
    }

    report_ac(total);
}
