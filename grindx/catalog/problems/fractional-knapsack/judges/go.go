        package main

        import (
	"encoding/json"
	"math"
)

        func main() {
	tc := LoadCases("fractional-knapsack")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var values, weights []int
	var cap int
	_ = json.Unmarshal(c.Input[0], &values)
	_ = json.Unmarshal(c.Input[1], &weights)
	_ = json.Unmarshal(c.Input[2], &cap)
	actual := fractionalKnapsack(append([]int(nil), values...), append([]int(nil), weights...), cap)
	var expected float64
	_ = json.Unmarshal(c.Expected, &expected)
	if math.Abs(actual - expected) > 1e-4 {
		ReportWA(i, []any{values, weights, cap}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
