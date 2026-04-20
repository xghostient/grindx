        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("max-combination-sum")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var a []int
	var b []int
	var k int
	_ = json.Unmarshal(c.Input[0], &a)
	_ = json.Unmarshal(c.Input[1], &b)
	_ = json.Unmarshal(c.Input[2], &k)
	actual := maxSumCombinations(append([]int(nil), a...), append([]int(nil), b...), k)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{a, b, k}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
