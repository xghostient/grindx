        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("longest-repeating-character-replacement")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	var k int
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &k)
	actual := characterReplacement(s, k)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{s, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
