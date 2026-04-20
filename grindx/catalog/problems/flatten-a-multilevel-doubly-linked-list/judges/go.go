package main

import "encoding/json"

type multiNodeSpec struct {
	Val   int             `json:"val"`
	Child []multiNodeSpec `json:"child,omitempty"`
}

func buildMultiLevel(spec []multiNodeSpec) *Node {
	if len(spec) == 0 {
		return nil
	}
	var head *Node
	var prev *Node
	for _, item := range spec {
		node := &Node{Val: item.Val}
		if head == nil {
			head = node
		}
		if prev != nil {
			prev.Next = node
			node.Prev = prev
		}
		if len(item.Child) > 0 {
			node.Child = buildMultiLevel(item.Child)
		}
		prev = node
	}
	return head
}

func multiToList(head *Node) []int {
	out := []int{}
	seen := map[*Node]struct{}{}
	var prev *Node
	for head != nil {
		if _, ok := seen[head]; ok || head.Prev != prev || head.Child != nil {
			return []int{linkedListSentinel}
		}
		seen[head] = struct{}{}
		out = append(out, head.Val)
		prev = head
		head = head.Next
	}
	return out
}

func main() {
	tc := LoadCases("flatten-a-multilevel-doubly-linked-list")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var spec []multiNodeSpec
		json.Unmarshal(c.Input[0], &spec)
		actual := multiToList(flatten(buildMultiLevel(spec)))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
