        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
	tc := LoadCases("plus-one")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var digits []int
	_ = json.Unmarshal(c.Input[0], &digits)
	actual := plusOne(append([]int(nil), digits...))
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, digits, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
