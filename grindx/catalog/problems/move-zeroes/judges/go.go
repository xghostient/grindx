        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("move-zeroes")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	moveZeroes(nums)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(nums, expected) {
		ReportWA(i, c.Input[0], expected, nums, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
