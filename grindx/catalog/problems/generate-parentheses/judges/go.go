        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

                        func sortedStrings(values []string) []string {
	out := append([]string(nil), values...)
	sort.Strings(out)
	return out
                }


        func main() {
	tc := LoadCases("generate-parentheses")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	_ = json.Unmarshal(c.Input[0], &n)
	actual := sortedStrings(generateParenthesis(n))
	var expected []string
	_ = json.Unmarshal(c.Expected, &expected)
	sort.Strings(expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, n, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
