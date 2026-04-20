        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

            func normalizeIntMatrix(rows [][]int) [][]int {
	out := make([][]int, len(rows))
	for i, row := range rows {
		copyRow := append([]int(nil), row...)
		sort.Ints(copyRow)
		out[i] = copyRow
	}
	sort.Slice(out, func(i, j int) bool {
		if len(out[i]) != len(out[j]) {
			return len(out[i]) < len(out[j])
		}
		for k := range out[i] {
			if out[i][k] != out[j][k] {
				return out[i][k] < out[j][k]
			}
		}
		return false
	})
	return out
    }


        func main() {
	tc := LoadCases("3sum")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	actual := normalizeIntMatrix(threeSum(append([]int(nil), nums...)))
	var expected [][]int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, nums, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
