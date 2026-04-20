        package main

        import (
	"encoding/json"
	"math"
)

        func main() {
        	tc := LoadCases("median-of-two-sorted-arrays")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums1, nums2 []int
	_ = json.Unmarshal(c.Input[0], &nums1)
	_ = json.Unmarshal(c.Input[1], &nums2)
	actual := findMedianSortedArrays(append([]int(nil), nums1...), append([]int(nil), nums2...))
	var expected float64
	_ = json.Unmarshal(c.Expected, &expected)
	if math.Abs(actual - expected) > 1e-5 {
		ReportWA(i, []any{nums1, nums2}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
