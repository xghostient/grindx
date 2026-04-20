        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("max-score-from-removing-substr")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	var x, y int
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &x)
	_ = json.Unmarshal(c.Input[2], &y)
	actual := maximumGain(s, x, y)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{s, x, y}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
