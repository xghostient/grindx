        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

        func normalizeStrList(items []string) []string {
	out := append([]string(nil), items...)
	sort.Strings(out)
	return out
}


        func main() {
	tc := LoadCases("generate-all-bin-strings")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	_ = json.Unmarshal(c.Input[0], &n)
	actual := normalizeStrList(generateBinaryStrings(n))
	var expected []string
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, n, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
