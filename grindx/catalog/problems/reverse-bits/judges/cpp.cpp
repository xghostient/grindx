    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("reverse-bits");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    uint32_t x = static_cast<uint32_t>(cases[i]["input"][0].get<long long>());
    uint32_t actual = reverseBits(x);
    uint32_t expected = static_cast<uint32_t>(cases[i]["expected"].get<long long>());
    if (actual != expected) report_wa(i, cases[i]["input"].to_string(), std::to_string(static_cast<unsigned long long>(expected)), std::to_string(static_cast<unsigned long long>(actual)), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
