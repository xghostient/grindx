        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("remove-k-digits")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var num string
	var k int
	_ = json.Unmarshal(c.Input[0], &num)
	_ = json.Unmarshal(c.Input[1], &k)
	actual := removeKdigits(num, k)
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{num, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
