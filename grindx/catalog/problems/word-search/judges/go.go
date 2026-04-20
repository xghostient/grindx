        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("word-search")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var board [][]byte
	var rawBoard [][]string
	_ = json.Unmarshal(c.Input[0], &rawBoard)
	board = make([][]byte, len(rawBoard))
	for r := range rawBoard {
		board[r] = make([]byte, len(rawBoard[r]))
		for cc := range rawBoard[r] {
			board[r][cc] = rawBoard[r][cc][0]
		}
	}
	var word string
	_ = json.Unmarshal(c.Input[1], &word)
	actual := exist(board, word)
	var expected bool
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{rawBoard, word}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
