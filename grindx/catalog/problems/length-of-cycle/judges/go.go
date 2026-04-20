package main

import "encoding/json"

func buildCycleList(values []int, pos int) *ListNode {
	if len(values) == 0 {
		return nil
	}
	head := &ListNode{Val: values[0]}
	nodes := []*ListNode{head}
	cur := head
	for _, v := range values[1:] {
		cur.Next = &ListNode{Val: v}
		cur = cur.Next
		nodes = append(nodes, cur)
	}
	if pos >= 0 {
		cur.Next = nodes[pos]
	}
	return head
}

func main() {
	tc := LoadCases("length-of-cycle")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var pos int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &pos)
		actual := cycleLength(buildCycleList(arr, pos))
		var expected int
		json.Unmarshal(c.Expected, &expected)
		if actual != expected {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
