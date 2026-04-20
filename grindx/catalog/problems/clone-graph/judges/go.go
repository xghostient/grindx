        package main

        import (
	"encoding/json"
	"sort"
        )

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix {
		result[i] = append([]int(nil), matrix[i]...)
	}
	return result
}

func decodeStringGrid(raw json.RawMessage) [][]byte {
	var rows []string
	_ = json.Unmarshal(raw, &rows)
	grid := make([][]byte, len(rows))
	for i, row := range rows {
		grid[i] = []byte(row)
	}
	return grid
}

func byteGridToStrings(grid [][]byte) []string {
	result := make([]string, len(grid))
	for i, row := range grid {
		result[i] = string(row)
	}
	return result
}

func normalizePairs(values [][]int) [][]int {
	result := make([][]int, len(values))
	for i, pair := range values {
		result[i] = append([]int(nil), pair...)
	}
	sort.Slice(result, func(i, j int) bool {
		if result[i][0] != result[j][0] {
			return result[i][0] < result[j][0]
		}
		return result[i][1] < result[j][1]
	})
	return result
}

func graphSharesIdentity(original *Node, clone *Node) bool {
	if original == nil || clone == nil {
		return false
	}
	originalNodes := map[*Node]struct{}{}
	queue := []*Node{original}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if _, ok := originalNodes[node]; ok {
			continue
		}
		originalNodes[node] = struct{}{}
		queue = append(queue, node.Neighbors...)
	}
	seen := map[*Node]struct{}{}
	queue = []*Node{clone}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if _, ok := seen[node]; ok {
			continue
		}
		if _, ok := originalNodes[node]; ok {
			return true
		}
		seen[node] = struct{}{}
		queue = append(queue, node.Neighbors...)
	}
	return false
}


        func main() {
	tc := LoadCases("clone-graph")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var adj [][]int
		_ = json.Unmarshal(c.Input[0], &adj)
		original := AdjListToGraph(adj)
		cloned := cloneGraph(original)
		if graphSharesIdentity(original, cloned) {
			ReportWA(i, adj, "deep copy without shared nodes", "shared original nodes", total, c.Category)
		}
		actual := GraphToAdjList(cloned)
		var expected [][]int
		_ = json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(i, adj, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
