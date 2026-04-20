        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("rabin-karp-repeated-string-match")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s, t string
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &t)
	actual := repeatedStringMatch(s, t)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{s, t}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
