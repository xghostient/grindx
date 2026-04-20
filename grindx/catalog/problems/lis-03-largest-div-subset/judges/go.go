        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("lis-03-largest-div-subset")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var arr []int
    	_ = json.Unmarshal(c.Input[0], &arr)
    	actual := largestDivisibleSubset(append([]int(nil), arr...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	valid := len(actual) == expected
    	seenVals := map[int]bool{}
    	inputVals := map[int]bool{}
    	for _, value := range arr {
    		inputVals[value] = true
    	}
    	if valid {
    		for _, value := range actual {
    			if seenVals[value] || !inputVals[value] {
    				valid = false
    				break
    			}
    			seenVals[value] = true
    		}
    	}
    	if valid {
    		for x := 0; x < len(actual); x++ {
    			for y := x + 1; y < len(actual); y++ {
    				if actual[x]%actual[y] != 0 && actual[y]%actual[x] != 0 {
    					valid = false
    				}
    			}
    		}
    	}
    	if !valid {
    		ReportWA(i, arr, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
