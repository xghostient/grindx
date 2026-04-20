        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("best-time-to-buy-and-sell-stock-iv")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var a int
    	var nums []int
    	_ = json.Unmarshal(c.Input[0], &a)
    	_ = json.Unmarshal(c.Input[1], &nums)
    	actual := maxProfit(a, append([]int(nil), nums...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{a, nums}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
