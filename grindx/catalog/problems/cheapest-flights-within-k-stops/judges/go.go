        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("cheapest-flights-within-k-stops")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var n int; _ = json.Unmarshal(c.Input[0], &n)
		var flights [][]int; _ = json.Unmarshal(c.Input[1], &flights)
		var src int; _ = json.Unmarshal(c.Input[2], &src)
		var dst int; _ = json.Unmarshal(c.Input[3], &dst)
		var k int; _ = json.Unmarshal(c.Input[4], &k)
		actual := findCheapestPrice(n, cloneMatrix(flights), src, dst, k)
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{n, flights, src, dst, k}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
