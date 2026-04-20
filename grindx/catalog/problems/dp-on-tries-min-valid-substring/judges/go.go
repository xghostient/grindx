        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("dp-on-tries-min-valid-substring")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	var dictionary []string
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &dictionary)
	actual := minExtraChar(s, dictionary)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{s, dictionary}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
