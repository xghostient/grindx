        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("count-bits-to-flip-a-to-b")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n, m int
	_ = json.Unmarshal(c.Input[0], &n)
	_ = json.Unmarshal(c.Input[1], &m)
	actual := minBitFlips(n, m)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{n, m}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
