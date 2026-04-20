        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("max-consecutive-ones-iii")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	var k int
	_ = json.Unmarshal(c.Input[0], &nums)
	_ = json.Unmarshal(c.Input[1], &k)
	actual := longestOnes(append([]int(nil), nums...), k)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{nums, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
