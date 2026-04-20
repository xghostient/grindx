        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix { result[i] = append([]int(nil), matrix[i]...) }
	return result
}


        func main() {
	tc := LoadCases("network-delay-time")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var times [][]int; _ = json.Unmarshal(c.Input[0], &times)
		var n int; _ = json.Unmarshal(c.Input[1], &n)
		var k int; _ = json.Unmarshal(c.Input[2], &k)
		actual := networkDelayTime(cloneMatrix(times), n, k)
		var expected int; _ = json.Unmarshal(c.Expected, &expected)
		if actual != expected { ReportWA(i, []any{times, n, k}, expected, actual, total, c.Category) }
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
