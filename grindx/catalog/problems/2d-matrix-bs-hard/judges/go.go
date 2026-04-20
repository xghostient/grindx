        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("2d-matrix-bs-hard")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var mat [][]int
	var target int
	_ = json.Unmarshal(c.Input[0], &mat)
	_ = json.Unmarshal(c.Input[1], &target)
	actual := searchMatrix(mat, target)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{mat, target}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
