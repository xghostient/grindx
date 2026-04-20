        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("sliding-window-maximum")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	var k int
	_ = json.Unmarshal(c.Input[0], &nums)
	_ = json.Unmarshal(c.Input[1], &k)
	actual := maxSlidingWindow(append([]int(nil), nums...), k)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if len(actual) != len(expected) {
		ReportWA(i, []any{nums, k}, expected, actual, total, c.Category)
	}
	for idx := range actual {
		if actual[idx] != expected[idx] {
			ReportWA(i, []any{nums, k}, expected, actual, total, c.Category)
		}
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
