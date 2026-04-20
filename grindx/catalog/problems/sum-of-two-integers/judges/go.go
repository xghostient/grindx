package main

import "encoding/json"

func main() {
	tc := LoadCases("sum-of-two-integers")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 int
		json.Unmarshal(c.Input[0], &arg0)
		var arg1 int
		json.Unmarshal(c.Input[1], &arg1)
		var expected int
		json.Unmarshal(c.Expected, &expected)

		result := getSum(arg0, arg1)

		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
