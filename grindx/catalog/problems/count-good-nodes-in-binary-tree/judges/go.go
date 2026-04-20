        package main

        import "encoding/json"

        func findNode(root *TreeNode, target int) *TreeNode {
	if root == nil {
		return nil
	}
	if root.Val == target {
		return root
	}
	left := findNode(root.Left, target)
	if left != nil {
		return left
	}
	return findNode(root.Right, target)
}

func inorderValues(root *TreeNode) []int {
	if root == nil {
		return []int{}
	}
	out := inorderValues(root.Left)
	out = append(out, root.Val)
	out = append(out, inorderValues(root.Right)...)
	return out
}

func preorderValues(root *TreeNode) []int {
	if root == nil {
		return []int{}
	}
	out := []int{root.Val}
	out = append(out, preorderValues(root.Left)...)
	out = append(out, preorderValues(root.Right)...)
	return out
}

func postorderValues(root *TreeNode) []int {
	if root == nil {
		return []int{}
	}
	out := postorderValues(root.Left)
	out = append(out, postorderValues(root.Right)...)
	out = append(out, root.Val)
	return out
}

func levelOrderValues(root *TreeNode) [][]int {
	if root == nil {
		return [][]int{}
	}
	out := [][]int{}
	queue := []struct {
		node  *TreeNode
		depth int
	}{{root, 0}}
	for len(queue) > 0 {
		item := queue[0]
		queue = queue[1:]
		if item.depth == len(out) {
			out = append(out, []int{})
		}
		out[item.depth] = append(out[item.depth], item.node.Val)
		if item.node.Left != nil {
			queue = append(queue, struct {
				node  *TreeNode
				depth int
			}{item.node.Left, item.depth + 1})
		}
		if item.node.Right != nil {
			queue = append(queue, struct {
				node  *TreeNode
				depth int
			}{item.node.Right, item.depth + 1})
		}
	}
	return out
}

func isBalancedTree(root *TreeNode) bool {
	var height func(*TreeNode) (int, bool)
	height = func(node *TreeNode) (int, bool) {
		if node == nil {
			return 0, true
		}
		leftHeight, leftOk := height(node.Left)
		rightHeight, rightOk := height(node.Right)
		if !leftOk || !rightOk || leftHeight-rightHeight > 1 || rightHeight-leftHeight > 1 {
			return 0, false
		}
		if leftHeight > rightHeight {
			return leftHeight + 1, true
		}
		return rightHeight + 1, true
	}
	_, ok := height(root)
	return ok
}


        func main() {
        	tc := LoadCases("count-good-nodes-in-binary-tree")
        	total := len(tc.Cases)
        for idx, c := range tc.Cases {
	var arr []interface{}
	var expected int
	json.Unmarshal(c.Input[0], &arr)
	json.Unmarshal(c.Expected, &expected)
	actual := goodNodes(ListToTree(arr))
	if actual != expected {
		ReportWA(idx, c.Input, expected, actual, total, c.Category)
	}
        	ReportProgress(idx + 1, total)
}

        	ReportAC(total)
        }
