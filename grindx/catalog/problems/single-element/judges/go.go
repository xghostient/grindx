        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("single-element")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	_ = json.Unmarshal(c.Input[0], &arr)
	actual := singleNonDuplicate(append([]int(nil), arr...))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, arr, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
