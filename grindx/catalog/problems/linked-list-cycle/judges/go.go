package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("linked-list-cycle")
	basicCases := tc.Cases

	total := len(basicCases) + 2

	// Run basic cases
	for idx, c := range basicCases {
		var values []int
		var pos int
		json.Unmarshal(c.Input[0], &values)
		json.Unmarshal(c.Input[1], &pos)

		head := buildCycleList(values, pos)
		result := hasCycle(head)

		var expected bool
		json.Unmarshal(c.Expected, &expected)

		if result != expected {
			ReportWA(idx, c.Input, expected, result, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}

	largeValues := make([]int, 10000)
	for k := 0; k < len(largeValues); k++ {
		largeValues[k] = ((k * 17) % 200001) - 100000
	}

	head := buildCycleList(largeValues, -1)
	result := hasCycle(head)

	if result != false {
		ReportWA(len(basicCases), "hidden input (10000 nodes, no cycle)", false, result, total, "stress")
	}

	head = buildCycleList(largeValues, 5000)
	result = hasCycle(head)

	if result != true {
		ReportWA(len(basicCases)+1, "hidden input (10000 nodes, cycle at pos=5000)", true, result, total, "stress")
	}

	ReportAC(total)
}

// buildCycleList builds a linked list from values and connects tail.Next
// to the node at index pos. If pos < 0, no cycle is created.
func buildCycleList(values []int, pos int) *ListNode {
	if len(values) == 0 {
		return nil
	}

	nodes := make([]*ListNode, len(values))
	for i, v := range values {
		nodes[i] = &ListNode{Val: v}
	}
	for i := 0; i < len(nodes)-1; i++ {
		nodes[i].Next = nodes[i+1]
	}

	if pos >= 0 && pos < len(nodes) {
		nodes[len(nodes)-1].Next = nodes[pos]
	}

	return nodes[0]
}
