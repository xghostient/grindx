        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("hand-of-straights")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var val int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &val)
	actual := isNStraightHand(append([]int(nil), arr...), val)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr, val}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
