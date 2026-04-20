        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("number-of-nges-to-the-right")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var queries []int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &queries)
	actual := countNGEs(append([]int(nil), arr...), append([]int(nil), queries...))
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{arr, queries}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
