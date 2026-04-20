        package main

        import (
	"encoding/json"
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

    func sortedInts(values []int) []int {
	out := append([]int(nil), values...)
	sort.Ints(out)
	return out
    }

    func stringsToBytes(values []string) []byte {
	out := make([]byte, len(values))
	for i, value := range values {
		if len(value) > 0 {
			out[i] = value[0]
		}
	}
	return out
    }


        func main() {
	tc := LoadCases("task-scheduler")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var tasks []string
	var n int
	_ = json.Unmarshal(c.Input[0], &tasks)
	_ = json.Unmarshal(c.Input[1], &n)
	actual := leastInterval(stringsToBytes(tasks), n)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{tasks, n}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
