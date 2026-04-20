        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("bellman-ford")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var V int; _ = json.Unmarshal(c.Input[0], &V)
		var edges [][]int; _ = json.Unmarshal(c.Input[1], &edges)
		var src int; _ = json.Unmarshal(c.Input[2], &src)
		actual := bellmanFord(V, cloneMatrix(edges), src)
		var expected []int; _ = json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") { ReportWA(i, []any{V, edges, src}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
