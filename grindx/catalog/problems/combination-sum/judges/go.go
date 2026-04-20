package main

import "encoding/json"

func main() {
	tc := LoadCases("combination-sum")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var arg1 int
		json.Unmarshal(c.Input[1], &arg1)
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)

		result := combinationSum(arg0Input, arg1)
		if result == nil {
			result = [][]int{}
		}
		actual := result
		if !Compare(actual, expected, "unordered_nested") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
