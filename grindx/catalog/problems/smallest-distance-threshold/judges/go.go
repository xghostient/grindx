        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("smallest-distance-threshold")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var n int; _ = json.Unmarshal(c.Input[0], &n)
		var edges [][]int; _ = json.Unmarshal(c.Input[1], &edges)
		var threshold int; _ = json.Unmarshal(c.Input[2], &threshold)
		actual := findTheCity(n, cloneMatrix(edges), threshold)
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{n, edges, threshold}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
