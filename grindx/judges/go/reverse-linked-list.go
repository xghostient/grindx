package main

import (
	"encoding/json"
	"math/rand"
)

func main() {
	tc := LoadCases("reverse-linked-list")
	basicCases := tc.Cases

	// Generate large case for TLE detection
	rng := rand.New(rand.NewSource(42))
	largeNums := make([]int, 5000)
	for k := 0; k < len(largeNums); k++ {
		largeNums[k] = rng.Intn(2000000001) - 1000000000
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
		ReportWA(len(basicCases), "large input (5000 elements)", reversed, resultArr, total, "tle")
	}

	ReportAC(total)
}
