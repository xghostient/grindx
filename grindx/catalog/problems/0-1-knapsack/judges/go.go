        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("0-1-knapsack")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var capacity int
    	var wt []int
    	var val []int
    	_ = json.Unmarshal(c.Input[0], &capacity)
    	_ = json.Unmarshal(c.Input[1], &wt)
    	_ = json.Unmarshal(c.Input[2], &val)
    	actual := knapsack(capacity, append([]int(nil), wt...), append([]int(nil), val...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{capacity, wt, val}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
