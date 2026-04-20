        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("mcm-02-min-cost-to-cut-stick")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var n int
    	var cuts []int
    	_ = json.Unmarshal(c.Input[0], &n)
    	_ = json.Unmarshal(c.Input[1], &cuts)
    	actual := minCost(n, append([]int(nil), cuts...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{n, cuts}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
