        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
        	tc := LoadCases("all-div-of-a-num")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	_ = json.Unmarshal(c.Input[0], &n)
	actual := allDivisors(n)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if expected == nil {
		expected = []int{}
	}
	if actual == nil {
		actual = []int{}
	}
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, n, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
