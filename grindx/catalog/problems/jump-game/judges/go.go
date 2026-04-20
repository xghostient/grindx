        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("jump-game")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var nums []int
    	_ = json.Unmarshal(c.Input[0], &nums)
    	actual := canJump(append([]int(nil), nums...))
    	var expected bool
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, nums, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
