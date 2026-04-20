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
	tc := LoadCases("climbing-stairs")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var n int
    	_ = json.Unmarshal(c.Input[0], &n)
    	actual := climbStairs(n)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, n, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
