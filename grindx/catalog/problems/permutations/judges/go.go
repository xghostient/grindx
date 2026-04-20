        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

        func normalizeIntMatrixKeepInner(rows [][]int) [][]int {
	out := make([][]int, len(rows))
	for i, row := range rows {
		out[i] = append([]int(nil), row...)
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
	tc := LoadCases("permutations")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var nums []int
	_ = json.Unmarshal(c.Input[0], &nums)
	actual := normalizeIntMatrixKeepInner(permute(append([]int(nil), nums...)))
	var expected [][]int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, nums, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
