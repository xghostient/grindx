        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix {
		result[i] = append([]int(nil), matrix[i]...)
	}
	return result
        }

        func main() {
	tc := LoadCases("unique-paths")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var m int
    	var n int
    	_ = json.Unmarshal(c.Input[0], &m)
    	_ = json.Unmarshal(c.Input[1], &n)
    	actual := uniquePaths(m, n)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{m, n}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
