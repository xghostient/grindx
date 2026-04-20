package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("reverse-linked-list")
	basicCases := tc.Cases

	largeNums := make([]int, 5000)
	for k := 0; k < len(largeNums); k++ {
		largeNums[k] = ((k * 73) % 1001) - 500
	}

	total := len(basicCases) + 1

	// Run basic cases
	for i, c := range basicCases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)

		head := ListToLinkedList(arr)
		result := reverseList(head)
		resultArr := LinkedListToList(result)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(resultArr, expected, "exact") {
			ReportWA(i, c.Input, expected, resultArr, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	// Run large case
	head := ListToLinkedList(largeNums)
	result := reverseList(head)
	resultArr := LinkedListToList(result)

	// Expected: reversed largeNums
	reversed := make([]int, len(largeNums))
	for k, v := range largeNums {
		reversed[len(largeNums)-1-k] = v
	}

	if !Compare(resultArr, reversed, "exact") {
		ReportWA(len(basicCases), "max input (5000 elements)", reversed, resultArr, total, "stress")
	}

	ReportAC(total)
}
