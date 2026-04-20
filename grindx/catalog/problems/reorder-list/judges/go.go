package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("reorder-list")
	basicCases := tc.Cases

	// Generate large hidden cases at the published bounds.
	largeEven := make([]int, 50000)
	for k := 0; k < len(largeEven); k++ {
		largeEven[k] = (k % 1000) + 1
	}
	largeOdd := make([]int, 49999)
	for k := 0; k < len(largeOdd); k++ {
		largeOdd[k] = ((k * 7) % 1000) + 1
	}

	largeEvenExpected := reorderSlice(largeEven)
	largeOddExpected := reorderSlice(largeOdd)

	total := len(basicCases) + 2

	// Run basic cases
	for idx, c := range basicCases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)

		head := ListToLinkedList(arr)
		reorderList(head)
		resultArr := LinkedListToList(head)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(resultArr, expected, "exact") {
			ReportWA(idx, c.Input, expected, resultArr, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}

	// Run hidden even-length case
	head := ListToLinkedList(largeEven)
	reorderList(head)
	resultArr := LinkedListToList(head)

	if !Compare(resultArr, largeEvenExpected, "exact") {
		ReportWA(len(basicCases), "hidden input (50000 elements)", largeEvenExpected, resultArr, total, "stress")
	}

	head = ListToLinkedList(largeOdd)
	reorderList(head)
	resultArr = LinkedListToList(head)

	if !Compare(resultArr, largeOddExpected, "exact") {
		ReportWA(len(basicCases)+1, "hidden input (49999 elements)", largeOddExpected, resultArr, total, "stress")
	}

	ReportAC(total)
}

// reorderSlice computes the expected reorder result for a slice.
// Pattern: L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...
func reorderSlice(nums []int) []int {
	n := len(nums)
	if n == 0 {
		return []int{}
	}
	result := make([]int, 0, n)
	lo, hi := 0, n-1
	for lo <= hi {
		result = append(result, nums[lo])
		if lo != hi {
			result = append(result, nums[hi])
		}
		lo++
		hi--
	}
	return result
}
