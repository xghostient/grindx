package main

import (
	"encoding/json"
	"sort"
)

func main() {
	tc := LoadCases("merge-two-sorted-lists")
	basicCases := tc.Cases

	// Generate hidden max-constraint correctness cases
	list2Only := make([]int, 50)
	for k := 0; k < len(list2Only); k++ {
		list2Only[k] = (((k * 7) + 3) % 201) - 100
	}
	sort.Ints(list2Only)

	largeA := make([]int, 25)
	largeB := make([]int, 25)
	for k := 0; k < len(largeA); k++ {
		largeA[k] = (((k * 9) + 1) % 201) - 100
		largeB[k] = (((k * 11) + 5) % 201) - 100
	}
	sort.Ints(largeA)
	sort.Ints(largeB)

	merged := append(append([]int{}, largeA...), largeB...)
	sort.Ints(merged)

	total := len(basicCases) + 2

	// Run basic cases
	for idx, c := range basicCases {
		var arr1 []int
		var arr2 []int
		json.Unmarshal(c.Input[0], &arr1)
		json.Unmarshal(c.Input[1], &arr2)

		list1 := ListToLinkedList(arr1)
		list2 := ListToLinkedList(arr2)
		result := mergeTwoLists(list1, list2)
		resultArr := LinkedListToList(result)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(resultArr, expected, "exact") {
			ReportWA(idx, c.Input, expected, resultArr, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}

	// Run hidden empty/non-empty case
	list2 := ListToLinkedList(list2Only)
	result := mergeTwoLists(nil, list2)
	resultArr := LinkedListToList(result)

	if !Compare(resultArr, list2Only, "exact") {
		ReportWA(len(basicCases), "hidden input (empty + 50 elements)", list2Only, resultArr, total, "stress")
	}

	// Run hidden balanced max-size case
	list1 := ListToLinkedList(largeA)
	list2 = ListToLinkedList(largeB)
	result = mergeTwoLists(list1, list2)
	resultArr = LinkedListToList(result)

	if !Compare(resultArr, merged, "exact") {
		ReportWA(len(basicCases)+1, "hidden input (25 + 25 sorted elements)", merged, resultArr, total, "stress")
	}

	ReportAC(total)
}
