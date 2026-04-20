        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("interleaving-string")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var a, b, d string
    	_ = json.Unmarshal(c.Input[0], &a)
    	_ = json.Unmarshal(c.Input[1], &b)
    	_ = json.Unmarshal(c.Input[2], &d)
    	actual := isInterleave(a, b, d)
    	var expected bool
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{a, b, d}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
