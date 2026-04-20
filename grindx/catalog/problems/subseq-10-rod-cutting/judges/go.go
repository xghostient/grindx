        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("subseq-10-rod-cutting")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var nums []int
    	var target int
    	_ = json.Unmarshal(c.Input[0], &nums)
    	_ = json.Unmarshal(c.Input[1], &target)
    	actual := rodCutting(append([]int(nil), nums...), target)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{nums, target}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
