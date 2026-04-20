        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("coin-change-ii")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var amount int
    	var nums []int
    	_ = json.Unmarshal(c.Input[0], &amount)
    	_ = json.Unmarshal(c.Input[1], &nums)
    	actual := change(amount, append([]int(nil), nums...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{amount, nums}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
