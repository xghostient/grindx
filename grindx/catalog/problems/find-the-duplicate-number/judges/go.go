package main

import "encoding/json"

func main() {
	tc := LoadCases("find-the-duplicate-number")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)
		actual := findDuplicate(arr)
		var expected int
		json.Unmarshal(c.Expected, &expected)
		if actual != expected {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
