        package main

        import (
	"encoding/json"
)

        func cloneStringSlice(values []string) []string {
return append([]string(nil), values...)
}


        func main() {
	tc := LoadCases("longest-common-prefix")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var strs []string
	_ = json.Unmarshal(c.Input[0], &strs)
	actual := longestCommonPrefix(cloneStringSlice(strs))
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, strs, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
