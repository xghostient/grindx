package main

import "encoding/json"

func main() {
	tc := LoadCases("reverse-nodes-in-k-group")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var value int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &value)
		actual := LinkedListToList(reverseKGroup(ListToLinkedList(arr), value))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
