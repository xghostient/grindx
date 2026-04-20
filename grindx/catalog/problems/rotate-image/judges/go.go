package main

import "encoding/json"

func copyIntMatrix(src [][]int) [][]int {
	out := make([][]int, len(src))
	for i := range src {
		out[i] = append([]int(nil), src[i]...)
	}
	return out
}

func main() {
	tc := LoadCases("rotate-image")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 [][]int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := copyIntMatrix(arg0)
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)

		rotate(arg0Input)
		actual := arg0Input
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
