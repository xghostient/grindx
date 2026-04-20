        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("asteroid-collision")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	actual := asteroidCollision(append([]int(nil), nums...))
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, nums, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
