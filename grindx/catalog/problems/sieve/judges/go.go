        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
        	tc := LoadCases("sieve")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	_ = json.Unmarshal(c.Input[0], &n)
	actual := sieve(n)
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
