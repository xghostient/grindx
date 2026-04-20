package main

import "encoding/json"

func buildList(values []int) *ListNode {
	if len(values) == 0 {
		return nil
	}
	head := &ListNode{Val: values[0]}
	cur := head
	for _, v := range values[1:] {
		cur.Next = &ListNode{Val: v}
		cur = cur.Next
	}
	return head
}

func listTail(head *ListNode) *ListNode {
	cur := head
	for cur != nil && cur.Next != nil {
		cur = cur.Next
	}
	return cur
}

func buildIntersection(a, b, shared []int) (*ListNode, *ListNode, *ListNode) {
	sharedHead := buildList(shared)
	headA := buildList(a)
	headB := buildList(b)
	if headA == nil {
		headA = sharedHead
	} else if sharedHead != nil {
		listTail(headA).Next = sharedHead
	}
	if headB == nil {
		headB = sharedHead
	} else if sharedHead != nil {
		listTail(headB).Next = sharedHead
	}
	return headA, headB, sharedHead
}

func main() {
	tc := LoadCases("intersection-of-two-linked-lists")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var a []int
		var b []int
		var shared []int
		json.Unmarshal(c.Input[0], &a)
		json.Unmarshal(c.Input[1], &b)
		json.Unmarshal(c.Input[2], &shared)
		headA, headB, sharedHead := buildIntersection(a, b, shared)
		result := getIntersectionNode(headA, headB)
		if result != sharedHead {
			ReportWA(idx, c.Input, shared, LinkedListToList(result), total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
