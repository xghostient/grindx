        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
	tc := LoadCases("job-seq-problem")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var jobs [][]int
	_ = json.Unmarshal(c.Input[0], &jobs)
	copyJobs := make([][]int, len(jobs))
	for j, row := range jobs {
		copyJobs[j] = append([]int(nil), row...)
	}
	actual := jobSequencing(copyJobs)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, jobs, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
