        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("merge-triplets-to-form-target-triplet")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var triplets [][]int
	var target []int
	_ = json.Unmarshal(c.Input[0], &triplets)
	_ = json.Unmarshal(c.Input[1], &target)
	copyTrips := make([][]int, len(triplets))
	for j, row := range triplets {
		copyTrips[j] = append([]int(nil), row...)
	}
	actual := mergeTriplets(copyTrips, append([]int(nil), target...))
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{triplets, target}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
