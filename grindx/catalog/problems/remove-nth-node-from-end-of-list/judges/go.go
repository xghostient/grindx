package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	tc := LoadCases("remove-nth-node-from-end-of-list")
	basicCases := tc.Cases

	// Generate hidden max-constraint cases with duplicates.
	largeNums := make([]int, 30)
	for k := 0; k < len(largeNums); k++ {
		largeNums[k] = (k * 7) % 11
	}
	hiddenNs := []int{30, 15, 1}
	total := len(basicCases) + len(hiddenNs)

	// Run basic cases
	for idx, c := range basicCases {
		var arr []int
		var n int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &n)

		head := ListToLinkedList(arr)
		result := removeNthFromEnd(head, n)
		resultArr := LinkedListToList(result)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(resultArr, expected, "exact") {
			ReportWA(idx, c.Input, expected, resultArr, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}

	// Run hidden cases
	for idx, hiddenN := range hiddenNs {
		head := ListToLinkedList(largeNums)
		result := removeNthFromEnd(head, hiddenN)
		resultArr := LinkedListToList(result)

		removeIdx := len(largeNums) - hiddenN
		expected := make([]int, 0, len(largeNums)-1)
		for k, v := range largeNums {
			if k != removeIdx {
				expected = append(expected, v)
			}
		}

		if !Compare(resultArr, expected, "exact") {
			ReportWA(len(basicCases)+idx, fmt.Sprintf("hidden input (30 elements, n=%d)", hiddenN), expected, resultArr, total, "stress")
		}
	}

	ReportAC(total)
}
