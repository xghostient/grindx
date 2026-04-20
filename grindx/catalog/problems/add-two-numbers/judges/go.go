package main

import "encoding/json"

func main() {
	tc := LoadCases("add-two-numbers")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arrA []int
		var arrB []int
		json.Unmarshal(c.Input[0], &arrA)
		json.Unmarshal(c.Input[1], &arrB)
		actual := LinkedListToList(addTwoNumbers(ListToLinkedList(arrA), ListToLinkedList(arrB)))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
