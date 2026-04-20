        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("find-all-anagrams-in-a-string")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s, p string
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &p)
	actual := findAnagrams(s, p)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !Compare(actual, expected, "exact") {
		ReportWA(i, []any{s, p}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
