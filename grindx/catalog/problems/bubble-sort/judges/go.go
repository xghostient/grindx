package main

import (
	"encoding/json"
	"reflect"
)

func main() {
	tc := LoadCases("bubble-sort")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var arr []int
		_ = json.Unmarshal(c.Input[0], &arr)
		actual := bubbleSort(append([]int(nil), arr...))
		var expected []int
		_ = json.Unmarshal(c.Expected, &expected)
		if !reflect.DeepEqual(actual, expected) {
			ReportWA(i, arr, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
}
