package main

import (
	"encoding/json"
)

func main() {
	tc := LoadCases("maximum-depth-of-binary-tree")
	basicCases := tc.Cases

	// Generate large complete binary tree for TLE detection
	depth := 14 // 2^14 - 1 = 16383 nodes
	n := (1 << depth) - 1
	largeArr := make([]interface{}, n)
	for k := 0; k < n; k++ {
		largeArr[k] = float64(k + 1)
	}

	total := len(basicCases) + 1

	// Run basic cases
	for i, c := range basicCases {
		var arr []interface{}
		json.Unmarshal(c.Input[0], &arr)

		root := ListToTree(arr)
		result := maxDepth(root)

		var expected int
		json.Unmarshal(c.Expected, &expected)

		if result != expected {
			ReportWA(i, c.Input, expected, result, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	// Run large case
	root := ListToTree(largeArr)
	result := maxDepth(root)
	if result != depth {
		ReportWA(len(basicCases), "large tree (16383 nodes)", depth, result, total, "tle")
	}

	ReportAC(total)
}
