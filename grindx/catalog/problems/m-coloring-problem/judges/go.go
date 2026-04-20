        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("m-coloring-problem")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	var edges [][]int
	var m int
	_ = json.Unmarshal(c.Input[0], &n)
	_ = json.Unmarshal(c.Input[1], &edges)
	_ = json.Unmarshal(c.Input[2], &m)
	actual := graphColoring(n, edges, m)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{n, edges, m}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
