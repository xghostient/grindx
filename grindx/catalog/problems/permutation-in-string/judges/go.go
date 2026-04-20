        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("permutation-in-string")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var a, b string
	_ = json.Unmarshal(c.Input[0], &a)
	_ = json.Unmarshal(c.Input[1], &b)
	actual := checkInclusion(a, b)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{a, b}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
