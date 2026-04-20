package main

import "encoding/json"

func buildCycleList(values []int, pos int) (*ListNode, []*ListNode) {
	if len(values) == 0 {
		return nil, nil
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
	return head, nodes
}

func main() {
	tc := LoadCases("linked-list-cycle-ii")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		var pos int
		json.Unmarshal(c.Input[0], &arr)
		json.Unmarshal(c.Input[1], &pos)
		head, nodes := buildCycleList(arr, pos)
		result := detectCycle(head)
		actual := -1
		for i, node := range nodes {
			if result == node {
				actual = i
				break
			}
		}
		var expected int
		json.Unmarshal(c.Expected, &expected)
		if actual != expected {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
