package main

import "encoding/json"

func main() {
	tc := LoadCases("rotate-list")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var value int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &value)
		actual := LinkedListToList(rotateRight(ListToLinkedList(arr), value))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
