        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("longest-common-subsequence")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var a string
    	var b string
    	_ = json.Unmarshal(c.Input[0], &a)
    	_ = json.Unmarshal(c.Input[1], &b)
    	actual := longestCommonSubsequence(a, b)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{a, b}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
