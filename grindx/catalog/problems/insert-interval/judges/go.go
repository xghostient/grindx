        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
	tc := LoadCases("insert-interval")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var intervals [][]int
	var newInterval []int
	_ = json.Unmarshal(c.Input[0], &intervals)
	_ = json.Unmarshal(c.Input[1], &newInterval)
	copyIvs := make([][]int, len(intervals))
	for j, iv := range intervals {
		copyIvs[j] = append([]int(nil), iv...)
	}
	actual := insert(copyIvs, append([]int(nil), newInterval...))
	var expected [][]int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{intervals, newInterval}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
