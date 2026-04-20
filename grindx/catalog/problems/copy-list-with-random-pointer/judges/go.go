package main

import "encoding/json"

type randomSpec [2]*int

func buildRandom(spec [][]*int) (*Node, []*Node) {
	if len(spec) == 0 {
		return nil, nil
	}
	nodes := make([]*Node, len(spec))
	for i, item := range spec {
		nodes[i] = &Node{Val: *item[0]}
	}
	for i := 0; i+1 < len(nodes); i++ {
		nodes[i].Next = nodes[i+1]
	}
	for i, item := range spec {
		if item[1] != nil {
			nodes[i].Random = nodes[*item[1]]
		}
	}
	return nodes[0], nodes
}

func randomRepr(head *Node) [][]any {
	nodes := []*Node{}
	index := map[*Node]int{}
	cur := head
	for cur != nil {
		index[cur] = len(nodes)
		nodes = append(nodes, cur)
		cur = cur.Next
	}
	out := make([][]any, len(nodes))
	for i, node := range nodes {
		var randomIdx any = nil
		if node.Random != nil {
			randomIdx = index[node.Random]
		}
		out[i] = []any{node.Val, randomIdx}
	}
	return out
}

func containsNode(nodes []*Node, target *Node) bool {
	for _, node := range nodes {
		if node == target {
			return true
		}
	}
	return false
}

func main() {
	tc := LoadCases("copy-list-with-random-pointer")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var spec [][]*int
		json.Unmarshal(c.Input[0], &spec)
		if len(spec) == 1 && len(spec[0]) == 0 {
			spec = [][]*int{}
		}
		head, originals := buildRandom(spec)
		result := copyRandomList(head)
		actual := randomRepr(result)
		deepOk := true
		for cur := result; cur != nil; cur = cur.Next {
			if containsNode(originals, cur) {
				deepOk = false
				break
			}
		}
		var expected [][]any
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") || !deepOk {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
