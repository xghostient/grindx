        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("peak-element")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	idx := findPeakElement(append([]int(nil), nums...))
	n := len(nums)
	valid := idx >= 0 && idx < n
	if valid && idx > 0 && nums[idx] <= nums[idx-1] {
		valid = false
	}
	if valid && idx < n-1 && nums[idx] <= nums[idx+1] {
		valid = false
	}
	if !valid {
		ReportWA(i, nums, "valid peak", idx, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
