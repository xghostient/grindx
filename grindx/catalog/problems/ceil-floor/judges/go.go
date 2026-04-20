        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
        	tc := LoadCases("ceil-floor")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	var x int
	_ = json.Unmarshal(c.Input[0], &arr)
	_ = json.Unmarshal(c.Input[1], &x)
	floor, ceil := findFloorCeil(append([]int(nil), arr...), x)
	actual := []int{floor, ceil}
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{arr, x}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
