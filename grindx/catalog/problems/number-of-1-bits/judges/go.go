        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("number-of-1-bits")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var x int
	_ = json.Unmarshal(c.Input[0], &x)
	actual := hammingWeight(x)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, x, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
