package main

import "encoding/json"

func main() {
	tc := LoadCases("middle-of-the-linked-list")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)
		actual := LinkedListToList(middleNode(ListToLinkedList(arr)))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
