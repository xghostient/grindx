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
	tc := LoadCases("combination-sum-ii")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var candidates []int
	var target int
	_ = json.Unmarshal(c.Input[0], &candidates)
	_ = json.Unmarshal(c.Input[1], &target)
	actual := normalizeIntMatrix(combinationSum2(append([]int(nil), candidates...), target))
	var expected [][]int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{candidates, target}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
