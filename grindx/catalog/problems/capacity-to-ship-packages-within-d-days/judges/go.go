        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("capacity-to-ship-packages-within-d-days")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var target int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &target)
	actual := shipWithinDays(append([]int(nil), arr...), target)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr, target}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
