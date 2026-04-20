        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("search-in-rotated-sorted-array-ii")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var target int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &target)
	actual := search(append([]int(nil), arr...), target)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr, target}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
