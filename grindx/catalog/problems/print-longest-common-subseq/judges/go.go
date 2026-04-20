        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("print-longest-common-subseq")
	total := len(tc.Cases)
            isSubsequence := func(needle string, haystack string) bool {
    	idx := 0
    	for _, ch := range haystack {
    		if idx < len(needle) && rune(needle[idx]) == ch {
    			idx++
    		}
    	}
    	return idx == len(needle)
    }

    for i, c := range tc.Cases {
    	var a, b string
    	_ = json.Unmarshal(c.Input[0], &a)
    	_ = json.Unmarshal(c.Input[1], &b)
    	actual := printLCS(a, b)
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if len(actual) != expected || !isSubsequence(actual, a) || !isSubsequence(actual, b) {
    		ReportWA(i, []any{a, b}, expected, actual, total, c.Category)
    	}
    	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
