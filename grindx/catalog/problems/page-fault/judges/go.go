        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("page-fault")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var val int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &val)
	actual := pageFaults(append([]int(nil), arr...), val)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr, val}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
