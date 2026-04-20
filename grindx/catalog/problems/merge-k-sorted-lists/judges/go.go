package main

import (
	"encoding/json"
	"sort"
)

func main() {
	tc := LoadCases("merge-k-sorted-lists")
	basicCases := tc.Cases

	// Generate hidden dense and sparse max-constraint cases.
	largeLists := make([][]int, 100)
	var allVals []int
	for i := 0; i < 100; i++ {
		list := make([]int, 100)
		for k := 0; k < 100; k++ {
			list[k] = (((i * 97) + (k * 29)) % 20001) - 10000
		}
		sort.Ints(list)
		largeLists[i] = list
		allVals = append(allVals, list...)
	}
	sort.Ints(allVals)

	singletonLists := make([][]int, 10000)
	singletonExpected := make([]int, 10000)
	for i := 0; i < 10000; i++ {
		value := ((i * 37) % 20001) - 10000
		singletonLists[i] = []int{value}
		singletonExpected[i] = value
	}
	sort.Ints(singletonExpected)

	sparseLists := make([][]int, 10000)
	sparseLists[123] = []int{-5, -5, 0, 3}
	sparseLists[5000] = []int{-1, 2, 2}
	sparseLists[9999] = []int{4}
	sparseExpected := []int{-5, -5, -1, 0, 2, 2, 3, 4}

	total := len(basicCases) + 3

	// Run basic cases
	for idx, c := range basicCases {
		var arrays [][]int
		json.Unmarshal(c.Input[0], &arrays)

		lists := make([]*ListNode, len(arrays))
		for k, arr := range arrays {
			lists[k] = ListToLinkedList(arr)
		}

		result := mergeKLists(lists)
		resultArr := LinkedListToList(result)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(resultArr, expected, "exact") {
			ReportWA(idx, c.Input, expected, resultArr, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}

	// Run dense hidden case
	lists := make([]*ListNode, len(largeLists))
	for k, arr := range largeLists {
		lists[k] = ListToLinkedList(arr)
	}

	result := mergeKLists(lists)
	resultArr := LinkedListToList(result)

	if !Compare(resultArr, allVals, "exact") {
		ReportWA(len(basicCases), "hidden input (100 lists x 100 elements)", allVals, resultArr, total, "stress")
	}

	// Run singleton hidden case
	lists = make([]*ListNode, len(singletonLists))
	for k, arr := range singletonLists {
		lists[k] = ListToLinkedList(arr)
	}

	result = mergeKLists(lists)
	resultArr = LinkedListToList(result)

	if !Compare(resultArr, singletonExpected, "exact") {
		ReportWA(len(basicCases)+1, "hidden input (10000 singleton lists)", singletonExpected, resultArr, total, "stress")
	}

	// Run sparse hidden case
	lists = make([]*ListNode, len(sparseLists))
	for k, arr := range sparseLists {
		lists[k] = ListToLinkedList(arr)
	}

	result = mergeKLists(lists)
	resultArr = LinkedListToList(result)

	if !Compare(resultArr, sparseExpected, "exact") {
		ReportWA(len(basicCases)+2, "hidden input (10000 lists, mostly empty)", sparseExpected, resultArr, total, "stress")
	}

	ReportAC(total)
}
