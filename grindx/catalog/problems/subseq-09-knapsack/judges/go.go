        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("subseq-09-knapsack")
	total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var n int
    	var capacity int
    	var profit []int
    	var weight []int
    	_ = json.Unmarshal(c.Input[0], &n)
    	_ = json.Unmarshal(c.Input[1], &capacity)
    	_ = json.Unmarshal(c.Input[2], &profit)
    	_ = json.Unmarshal(c.Input[3], &weight)
    	actual := unboundedKnapsack(n, capacity, append([]int(nil), profit...), append([]int(nil), weight...))
    	var expected int
    	_ = json.Unmarshal(c.Expected, &expected)
    	if actual != expected {
    		ReportWA(i, []any{n, capacity, profit, weight}, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	ReportAC(total)
        }
