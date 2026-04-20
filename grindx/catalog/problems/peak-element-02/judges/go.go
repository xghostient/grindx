        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("peak-element-02")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var mat [][]int
	_ = json.Unmarshal(c.Input[0], &mat)
	result := findPeakGrid(mat)
	rows, cols := len(mat), len(mat[0])
	valid := len(result) == 2
	var r, cc int
	if valid {
		r, cc = result[0], result[1]
		valid = r >= 0 && r < rows && cc >= 0 && cc < cols
	}
	if valid {
		val := mat[r][cc]
		if r > 0 && mat[r-1][cc] >= val {
			valid = false
		}
		if r < rows-1 && mat[r+1][cc] >= val {
			valid = false
		}
		if cc > 0 && mat[r][cc-1] >= val {
			valid = false
		}
		if cc < cols-1 && mat[r][cc+1] >= val {
			valid = false
		}
	}
	if !valid {
		ReportWA(i, mat, "valid 2D peak", result, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
