        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("mst-kruskal-algo")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var V int; _ = json.Unmarshal(c.Input[0], &V)
		var edges [][]int; _ = json.Unmarshal(c.Input[1], &edges)
		actual := kruskalMST(V, cloneMatrix(edges))
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{V, edges}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
