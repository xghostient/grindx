package main

import "encoding/json"

func main() {
	tc := LoadCases("split-linked-list-in-parts")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var k int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &k)
		parts := splitListToParts(ListToLinkedList(arr), k)
		actual := make([][]int, len(parts))
		for i, node := range parts {
			actual[i] = LinkedListToList(node)
		}
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
