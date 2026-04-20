        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("non-overlapping-intervals")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var intervals [][]int
	_ = json.Unmarshal(c.Input[0], &intervals)
	copyIvs := make([][]int, len(intervals))
	for j, iv := range intervals {
		copyIvs[j] = append([]int(nil), iv...)
	}
	actual := eraseOverlapIntervals(copyIvs)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, intervals, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
