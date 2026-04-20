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
	tc := LoadCases("dp-square-count-submatrics")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var matrix [][]int
    	_ = json.Unmarshal(c.Input[0], &matrix)
    	actual := countSquares(cloneMatrix(matrix))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, matrix, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
