        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("word-break")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var s string
    	var words []string
    	_ = json.Unmarshal(c.Input[0], &s)
    	_ = json.Unmarshal(c.Input[1], &words)
    	actual := wordBreak(s, append([]string(nil), words...))
    	var expected bool
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{s, words}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
