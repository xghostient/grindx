        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("median-in-matrix")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var mat [][]int
	_ = json.Unmarshal(c.Input[0], &mat)
	actual := findMedian(mat)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, mat, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
