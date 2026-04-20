        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("min-multiplications-to-reach-end")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arr []int; _ = json.Unmarshal(c.Input[0], &arr)
		var start int; _ = json.Unmarshal(c.Input[1], &start)
		var end int; _ = json.Unmarshal(c.Input[2], &end)
		actual := minimumMultiplications(arr, start, end)
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{arr, start, end}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
