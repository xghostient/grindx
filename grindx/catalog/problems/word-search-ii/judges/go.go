        package main

        import (
	"encoding/json"
	"reflect"
	"sort"
)

        func main() {
	tc := LoadCases("word-search-ii")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var board [][]byte
	var rawBoard [][]string
	_ = json.Unmarshal(c.Input[0], &rawBoard)
	board = make([][]byte, len(rawBoard))
	for r, row := range rawBoard {
		board[r] = make([]byte, len(row))
		for ci, ch := range row {
			if len(ch) > 0 {
				board[r][ci] = ch[0]
			}
		}
	}
	var words []string
	_ = json.Unmarshal(c.Input[1], &words)
	actual := findWords(board, words)
	sort.Strings(actual)
	var expected []string
	_ = json.Unmarshal(c.Expected, &expected)
	sort.Strings(expected)
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []any{rawBoard, words}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
