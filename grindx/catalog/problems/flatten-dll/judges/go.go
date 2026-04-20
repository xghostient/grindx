package main

import "encoding/json"

func buildBottom(rows [][]int) *Node {
	if len(rows) == 0 {
		return nil
	}
	heads := []*Node{}
	for _, row := range rows {
		if len(row) == 0 {
			continue
		}
		head := &Node{Val: row[0]}
		cur := head
		for _, value := range row[1:] {
			cur.Bottom = &Node{Val: value}
			cur = cur.Bottom
		}
		heads = append(heads, head)
	}
	for i := 0; i+1 < len(heads); i++ {
		heads[i].Next = heads[i+1]
	}
	if len(heads) == 0 {
		return nil
	}
	return heads[0]
}

func bottomToList(head *Node) []int {
	out := []int{}
	seen := map[*Node]struct{}{}
	for head != nil {
		if _, ok := seen[head]; ok {
			return []int{linkedListSentinel}
		}
		seen[head] = struct{}{}
		out = append(out, head.Val)
		head = head.Bottom
	}
	return out
}

func main() {
	tc := LoadCases("flatten-dll")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var rows [][]int
		json.Unmarshal(c.Input[0], &rows)
		if len(rows) == 1 && len(rows[0]) == 0 {
			rows = [][]int{}
		}
		actual := bottomToList(flatten(buildBottom(rows)))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
