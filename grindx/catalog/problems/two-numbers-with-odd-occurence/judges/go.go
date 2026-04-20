        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

        func main() {
        	tc := LoadCases("two-numbers-with-odd-occurence")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr []int
	_ = json.Unmarshal(c.Input[0], &arr)
	actual := twoOddOccurrences(append([]int(nil), arr...))
	sort.Ints(actual)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, arr, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
