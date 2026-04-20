package main

import (
	"encoding/json"
	"sort"
)

func listToDLL(arr []int) *DLLNode {
	if len(arr) == 0 {
		return nil
	}
	head := &DLLNode{Val: arr[0]}
	cur := head
	for _, v := range arr[1:] {
		node := &DLLNode{Val: v, Prev: cur}
		cur.Next = node
		cur = node
	}
	return head
}

func normalizePairs(result [][]int) [][]int {
	out := make([][]int, len(result))
	for i, pair := range result {
		row := []int{pair[0], pair[1]}
		out[i] = row
	}
	sort.Slice(out, func(i, j int) bool {
		if out[i][0] != out[j][0] {
			return out[i][0] < out[j][0]
		}
		return out[i][1] < out[j][1]
	})
	return out
}

func main() {
	tc := LoadCases("pairs-in-dll")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var target int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &target)
		actual := normalizePairs(findPairs(listToDLL(arr), target))
		var expected [][]int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
