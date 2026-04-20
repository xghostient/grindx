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
	tc := LoadCases("minimal-cost")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var heights []int
    	var k int
    	_ = json.Unmarshal(c.Input[0], &heights)
    	_ = json.Unmarshal(c.Input[1], &k)
    	actual := minimalCost(append([]int(nil), heights...), k)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{heights, k}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
