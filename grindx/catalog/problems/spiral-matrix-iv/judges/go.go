package main

import "encoding/json"

func main() {
	tc := LoadCases("spiral-matrix-iv")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 int
		json.Unmarshal(c.Input[0], &arg0)
		var arg1 int
		json.Unmarshal(c.Input[1], &arg1)
		var arg2 []int
		json.Unmarshal(c.Input[2], &arg2)
		arg2Head := ListToLinkedList(arg2)
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)

		result := spiralMatrix(arg0, arg1, arg2Head)
		if result == nil {
			result = [][]int{}
		}
		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
