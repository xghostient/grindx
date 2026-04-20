        package main

        import (
	"encoding/json"
	"math"
)

        func main() {
	tc := LoadCases("shortest-job-first")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	_ = json.Unmarshal(c.Input[0], &arr)
	actual := sjfAvgWait(append([]int(nil), arr...))
	var expected float64
	_ = json.Unmarshal(c.Expected, &expected)
	if math.Abs(actual - expected) > 1e-4 {
		ReportWA(i, arr, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
