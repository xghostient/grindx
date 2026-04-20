package main

import "encoding/json"

func main() {
	tc := LoadCases("pascals-triangle")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 int
		json.Unmarshal(c.Input[0], &arg0)
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)

		result := generate(arg0)
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
