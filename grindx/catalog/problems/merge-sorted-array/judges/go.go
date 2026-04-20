        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("merge-sorted-array")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums1, nums2 []int
	var m, n int
	_ = json.Unmarshal(c.Input[0], &nums1)
	_ = json.Unmarshal(c.Input[1], &m)
	_ = json.Unmarshal(c.Input[2], &nums2)
	_ = json.Unmarshal(c.Input[3], &n)
	merge(nums1, m, append([]int(nil), nums2...), n)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(nums1, expected) {
		ReportWA(i, []any{nums1, m, nums2, n}, expected, nums1, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
