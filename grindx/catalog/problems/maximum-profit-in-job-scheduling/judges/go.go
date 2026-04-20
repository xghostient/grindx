        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("maximum-profit-in-job-scheduling")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var startTime, endTime, profit []int
	_ = json.Unmarshal(c.Input[0], &startTime)
	_ = json.Unmarshal(c.Input[1], &endTime)
	_ = json.Unmarshal(c.Input[2], &profit)
	actual := jobScheduling(append([]int(nil), startTime...), append([]int(nil), endTime...), append([]int(nil), profit...))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{startTime, endTime, profit}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
