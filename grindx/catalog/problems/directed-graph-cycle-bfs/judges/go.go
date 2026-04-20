        package main

        import "encoding/json"

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix {
		result[i] = append([]int(nil), matrix[i]...)
	}
	return result
}

func validTopologicalOrder(order []int, v int, adj [][]int) bool {
	if len(order) != v {
		return false
	}
	pos := make([]int, v)
	seen := make([]bool, v)
	for idx, node := range order {
		if node < 0 || node >= v || seen[node] {
			return false
		}
		seen[node] = true
		pos[node] = idx
	}
	for node := 0; node < v; node++ {
		if !seen[node] {
			return false
		}
		for _, nei := range adj[node] {
			if pos[node] >= pos[nei] {
				return false
			}
		}
	}
	return true
}

func validCourseOrder(order []int, numCourses int, prerequisites [][]int) bool {
	if len(order) != numCourses {
		return false
	}
	pos := make([]int, numCourses)
	seen := make([]bool, numCourses)
	for idx, course := range order {
		if course < 0 || course >= numCourses || seen[course] {
			return false
		}
		seen[course] = true
		pos[course] = idx
	}
	for _, edge := range prerequisites {
		if pos[edge[1]] >= pos[edge[0]] {
			return false
		}
	}
	return true
}


        func main() {
	tc := LoadCases("directed-graph-cycle-bfs")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var v int
		_ = json.Unmarshal(c.Input[0], &v)
		var adj [][]int
		_ = json.Unmarshal(c.Input[1], &adj)
		actual := isCyclic(v, cloneMatrix(adj))
		var expected bool
		_ = json.Unmarshal(c.Expected, &expected)
		if actual != expected {
			ReportWA(i, []any{v, adj}, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
