        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("lis-02-print-lis")
	total := len(tc.Cases)
            isSubsequenceList := func(seq []int, arr []int) bool {
    	idx := 0
    	for _, value := range arr {
    		if idx < len(seq) && seq[idx] == value {
    			idx++
    		}
    	}
    	return idx == len(seq)
    }

    for i, c := range tc.Cases {
    	var arr []int
    	_ = json.Unmarshal(c.Input[0], &arr)
    	actual := printLIS(append([]int(nil), arr...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	valid := len(actual) == expected
    	if valid {
    		for j := 0; j+1 < len(actual); j++ {
    			if actual[j] >= actual[j+1] {
    				valid = false
    				break
    			}
    		}
    		if valid && !isSubsequenceList(actual, arr) {
    			valid = false
    		}
    	}
    	if !valid {
    		ReportWA(i, arr, expected, actual, total, c.Category)
    	}
    	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
