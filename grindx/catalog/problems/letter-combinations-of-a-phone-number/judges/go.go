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
	tc := LoadCases("letter-combinations-of-a-phone-number")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var digits string
	_ = json.Unmarshal(c.Input[0], &digits)
	actual := normalizeStrList(letterCombinations(digits))
	var expected []string
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, digits, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
