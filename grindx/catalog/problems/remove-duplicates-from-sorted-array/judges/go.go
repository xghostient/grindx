        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("remove-duplicates-from-sorted-array")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	actualK := removeDuplicates(nums)
	var expected struct {
		K int `json:"k"`
		Prefix []int `json:"prefix"`
	}
	_ = json.Unmarshal(c.Expected, &expected)
	actual := map[string]any{"k": actualK, "prefix": []int{}}
	if actualK >= 0 && actualK <= len(nums) {
		actual["prefix"] = append([]int(nil), nums[:actualK]...)
	}
	if actualK != expected.K || !reflect.DeepEqual(actual["prefix"], expected.Prefix) {
		ReportWA(i, c.Input[0], expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
