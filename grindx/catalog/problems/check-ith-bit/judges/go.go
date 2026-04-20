        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("check-ith-bit")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n, k int
	_ = json.Unmarshal(c.Input[0], &n)
	_ = json.Unmarshal(c.Input[1], &k)
	actual := checkIthBit(n, k)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{n, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
