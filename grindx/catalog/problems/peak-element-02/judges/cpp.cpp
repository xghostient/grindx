    #include "_common.h"
    #include "solution.cpp"

    int main() {
        auto tc = load_cases("peak-element-02");
        auto& cases = tc["cases"].get_array();
        int total = static_cast<int>(cases.size());
        for (int i = 0; i < total; i++) {
    auto mat = cases[i]["input"][0].get<std::vector<std::vector<int>>>();
    auto result = findPeakGrid(mat);
    int rows = static_cast<int>(mat.size()), cols = static_cast<int>(mat[0].size());
    bool valid = result.size() == 2;
    int r = 0, cc = 0;
    if (valid) {
        r = result[0];
        cc = result[1];
        valid = r >= 0 && r < rows && cc >= 0 && cc < cols;
    }
    if (valid) {
        int val = mat[r][cc];
        if (r > 0 && mat[r - 1][cc] >= val) valid = false;
        if (r < rows - 1 && mat[r + 1][cc] >= val) valid = false;
        if (cc > 0 && mat[r][cc - 1] >= val) valid = false;
        if (cc < cols - 1 && mat[r][cc + 1] >= val) valid = false;
    }
    if (!valid) report_wa(i, cases[i]["input"].to_string(), "valid 2D peak", json::Value(result).to_string(), total, cases[i]["category"].is_string() ? cases[i]["category"].get_string() : "");
    report_progress(i + 1, total);
}
        report_ac(total);
    }
