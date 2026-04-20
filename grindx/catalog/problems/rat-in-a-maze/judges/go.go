        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

        func normalizeStrList(items []string) []string {
	out := append([]string(nil), items...)
	sort.Strings(out)
	return out
}


        func main() {
	tc := LoadCases("rat-in-a-maze")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var maze [][]int
	_ = json.Unmarshal(c.Input[0], &maze)
	mCopy := make([][]int, len(maze))
	for r := range maze {
		mCopy[r] = append([]int(nil), maze[r]...)
	}
	actual := normalizeStrList(findPath(mCopy))
	var expected []string
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, maze, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
