        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("lis-06-longest-string-chain")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var words []string
    	_ = json.Unmarshal(c.Input[0], &words)
    	actual := longestStrChain(append([]string(nil), words...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, words, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
