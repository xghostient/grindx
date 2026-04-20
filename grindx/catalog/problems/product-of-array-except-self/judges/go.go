package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("product-of-array-except-self")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var expected []int
		json.Unmarshal(c.Expected, &expected)

		result := productExceptSelf(arg0Input)
		if !Compare(result, expected, "exact") {
			ReportWA(i, c.Input, expected, result, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
