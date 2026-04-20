            package main

            import "encoding/json"

            func listToDLL(arr []int) (*DLLNode, []*DLLNode) {
            	if len(arr) == 0 {
            		return nil, nil
            	}
            	head := &DLLNode{Val: arr[0]}
            	nodes := []*DLLNode{head}
            	cur := head
            	for _, v := range arr[1:] {
            		node := &DLLNode{Val: v, Prev: cur}
            		cur.Next = node
            		cur = node
            		nodes = append(nodes, cur)
            	}
            	return head, nodes
            }

            func dllToList(head *DLLNode) []int {
            	out := []int{}
            	seen := map[*DLLNode]struct{}{}
            	var prev *DLLNode
            	for head != nil {
            		if _, ok := seen[head]; ok || head.Prev != prev {
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
            	tc := LoadCases("insert-node-dll")
            	total := len(tc.Cases)
            	for idx, c := range tc.Cases {
            		var arr []int
            		json.Unmarshal(c.Input[0], &arr)
            		head, _ := listToDLL(arr)
		var pos int
		var value int
		json.Unmarshal(c.Input[1], &pos)
		json.Unmarshal(c.Input[2], &value)
		actual := dllToList(insertNode(head, pos, value))
            		var expected []int
            		json.Unmarshal(c.Expected, &expected)
            		if !Compare(actual, expected, "exact") {
            			ReportWA(idx, c.Input, expected, actual, total, c.Category)
            		}
            		ReportProgress(idx + 1, total)
            	}
            	ReportAC(total)
            }
