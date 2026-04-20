        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("sudoku-solver")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var rawBoard [][]string
	_ = json.Unmarshal(c.Input[0], &rawBoard)
	board := make([][]byte, 9)
	for r := 0; r < 9; r++ {
		board[r] = make([]byte, 9)
		for cc := 0; cc < 9; cc++ {
			board[r][cc] = rawBoard[r][cc][0]
		}
	}
	solveSudoku(board)
	var expectedBoard [][]string
	_ = json.Unmarshal(c.Expected, &expectedBoard)
	resultBoard := make([][]string, 9)
	for r := 0; r < 9; r++ {
		resultBoard[r] = make([]string, 9)
		for cc := 0; cc < 9; cc++ {
			resultBoard[r][cc] = string(board[r][cc])
		}
	}
	if !reflect.DeepEqual(resultBoard, expectedBoard) {
		ReportWA(i, rawBoard, expectedBoard, resultBoard, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
