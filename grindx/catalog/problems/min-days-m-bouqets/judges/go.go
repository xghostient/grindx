        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("min-days-m-bouqets")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var m, k int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &m)
	_ = json.Unmarshal(c.Input[2], &k)
	actual := minDays(append([]int(nil), arr...), m, k)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr, m, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
