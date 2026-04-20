package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("subarray-sum-equals-k")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var arg1 int
		json.Unmarshal(c.Input[1], &arg1)
		var expected int
		json.Unmarshal(c.Expected, &expected)

		result := subarraySum(arg0Input, arg1)
		if !Compare(result, expected, "exact") {
			ReportWA(i, c.Input, expected, result, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
