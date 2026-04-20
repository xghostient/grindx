        package main

        import (
	"encoding/json"
	"math"
)

        func main() {
	tc := LoadCases("pow-x-n")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var x float64
	var n int
	_ = json.Unmarshal(c.Input[0], &x)
	_ = json.Unmarshal(c.Input[1], &n)
	actual := myPow(x, n)
	var expected float64
	_ = json.Unmarshal(c.Expected, &expected)
	pass := false
	if !math.IsNaN(actual) && !math.IsInf(actual, 0) {
		diff := math.Abs(actual - expected)
		pass = diff <= 1e-5 || diff/math.Max(math.Abs(expected), 1e-9) <= 1e-5
	}
	if !pass {
		ReportWA(i, []any{x, n}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
