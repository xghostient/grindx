        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("decode-ways")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var s string
    	_ = json.Unmarshal(c.Input[0], &s)
    	actual := numDecodings(s)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, s, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
