        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("mst-prims-algorithm")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var V int; _ = json.Unmarshal(c.Input[0], &V)
		var adj [][][2]int; _ = json.Unmarshal(c.Input[1], &adj)
		actual := spanningTree(V, adj)
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{V, adj}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
