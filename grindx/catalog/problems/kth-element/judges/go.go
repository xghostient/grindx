package main

import "encoding/json"

func main() {
	tc := LoadCases("kth-element")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var arg1 []int
		json.Unmarshal(c.Input[1], &arg1)
		arg1Input := append([]int(nil), arg1...)
		var arg2 int
		json.Unmarshal(c.Input[2], &arg2)
		var expected int
		json.Unmarshal(c.Expected, &expected)

		result := kthElement(arg0Input, arg1Input, arg2)

		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
