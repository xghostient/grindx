        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("better-string")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s1, s2 string
	_ = json.Unmarshal(c.Input[0], &s1)
	_ = json.Unmarshal(c.Input[1], &s2)
	actual := betterString(s1, s2)
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{s1, s2}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
