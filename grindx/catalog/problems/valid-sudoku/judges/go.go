package main

import "encoding/json"

func main() {
	tc := LoadCases("valid-sudoku")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0Rows []string
		json.Unmarshal(c.Input[0], &arg0Rows)
		arg0 := make([][]byte, len(arg0Rows))
		for r := range arg0Rows {
			arg0[r] = []byte(arg0Rows[r])
		}
		var expected bool
		json.Unmarshal(c.Expected, &expected)

		result := isValidSudoku(arg0)

		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
