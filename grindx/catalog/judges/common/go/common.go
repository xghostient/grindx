package main

import (
	"encoding/json"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"sort"
)

var progressFile *os.File

// ---------------------------------------------------------------------------
// Data structures
// ---------------------------------------------------------------------------

type ListNode struct {
	Val  int
	Next *ListNode
}

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

type Node struct {
	Val       int
	Neighbors []*Node
	Next      *Node
	Random    *Node
	Prev      *Node
	Child     *Node
	Bottom    *Node
}

const linkedListSentinel = -2147483648

func ListToLinkedList(arr []int) *ListNode {
	if len(arr) == 0 {
		return nil
	}
	head := &ListNode{Val: arr[0]}
	curr := head
	for _, v := range arr[1:] {
		curr.Next = &ListNode{Val: v}
		curr = curr.Next
	}
	return head
}

func LinkedListToList(head *ListNode) []int {
	result := []int{}
	seen := map[*ListNode]struct{}{}
	steps := 0
	for head != nil && steps < 100000 {
		if _, ok := seen[head]; ok {
			result = append(result, linkedListSentinel)
			return result
		}
		seen[head] = struct{}{}
		result = append(result, head.Val)
		head = head.Next
		steps++
	}
	if head != nil {
		result = append(result, linkedListSentinel)
	}
	return result
}

func ListToTree(arr []interface{}) *TreeNode {
	if len(arr) == 0 || arr[0] == nil {
		return nil
	}
	root := &TreeNode{Val: toIntVal(arr[0])}
	queue := []*TreeNode{root}
	i := 1
	for len(queue) > 0 && i < len(arr) {
		node := queue[0]
		queue = queue[1:]
		if i < len(arr) && arr[i] != nil {
			node.Left = &TreeNode{Val: toIntVal(arr[i])}
			queue = append(queue, node.Left)
		}
		i++
		if i < len(arr) && arr[i] != nil {
			node.Right = &TreeNode{Val: toIntVal(arr[i])}
			queue = append(queue, node.Right)
		}
		i++
	}
	return root
}

func TreeToList(root *TreeNode) []interface{} {
	if root == nil {
		return []interface{}{}
	}
	result := []interface{}{}
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if node == nil {
			result = append(result, nil)
		} else {
			result = append(result, node.Val)
			queue = append(queue, node.Left)
			queue = append(queue, node.Right)
		}
	}
	for len(result) > 0 && result[len(result)-1] == nil {
		result = result[:len(result)-1]
	}
	return result
}

func toIntVal(v interface{}) int {
	switch val := v.(type) {
	case float64:
		return int(val)
	case json.Number:
		n, _ := val.Int64()
		return int(n)
	case int:
		return val
	default:
		return 0
	}
}

func AdjListToGraph(adjList [][]int) *Node {
	if len(adjList) == 0 {
		return nil
	}
	nodes := make(map[int]*Node, len(adjList))
	for i := 1; i <= len(adjList); i++ {
		nodes[i] = &Node{Val: i}
	}
	for i, neighbors := range adjList {
		for _, nb := range neighbors {
			nodes[i+1].Neighbors = append(nodes[i+1].Neighbors, nodes[nb])
		}
	}
	return nodes[1]
}

func GraphToAdjList(node *Node) [][]int {
	if node == nil {
		return [][]int{}
	}
	visited := map[int]*Node{}
	queue := []*Node{node}
	visited[node.Val] = node
	for len(queue) > 0 {
		n := queue[0]
		queue = queue[1:]
		for _, nb := range n.Neighbors {
			if _, ok := visited[nb.Val]; !ok {
				visited[nb.Val] = nb
				queue = append(queue, nb)
			}
		}
	}
	maxVal := 0
	for v := range visited {
		if v > maxVal {
			maxVal = v
		}
	}
	result := make([][]int, maxVal)
	for i := 1; i <= maxVal; i++ {
		if n, ok := visited[i]; ok {
			vals := []int{}
			for _, nb := range n.Neighbors {
				vals = append(vals, nb.Val)
			}
			sort.Ints(vals)
			result[i-1] = vals
		} else {
			result[i-1] = []int{}
		}
	}
	return result
}

// ---------------------------------------------------------------------------
// Test case loading
// ---------------------------------------------------------------------------

type TestCase struct {
	Input      []json.RawMessage `json:"input"`
	Expected   json.RawMessage   `json:"expected"`
	Operations []string          `json:"operations,omitempty"`
	OpInputs   []json.RawMessage `json:"op_inputs,omitempty"`
	Category   string            `json:"category"`
}

type TestData struct {
	ProblemID  string     `json:"problem_id"`
	Function   string     `json:"function"`
	Pattern    string     `json:"pattern"`
	Comparison string     `json:"comparison"`
	TimeLimitS float64    `json:"time_limit_s"`
	Cases      []TestCase `json:"cases"`
}

func LoadCases(problemID string) TestData {
	exe, _ := os.Executable()
	dir := filepath.Dir(exe)
	path := filepath.Join(dir, problemID+".json")
	data, err := os.ReadFile(path)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Cannot read test cases: %v\n", err)
		os.Exit(2)
	}
	var td TestData
	if err := json.Unmarshal(data, &td); err != nil {
		fmt.Fprintf(os.Stderr, "Cannot parse test cases: %v\n", err)
		os.Exit(2)
	}
	return td
}

// ---------------------------------------------------------------------------
// Comparison
// ---------------------------------------------------------------------------

func Compare(actual, expected any, mode string) bool {
	switch mode {
	case "exact":
		return jsonEqual(actual, expected)
	case "unordered":
		return unorderedEqual(actual, expected)
	case "unordered_nested":
		return unorderedNestedEqual(actual, expected)
	case "float_tolerance":
		a, aOk := toFloat(actual)
		e, eOk := toFloat(expected)
		return aOk && eOk && math.Abs(a-e) < 1e-5
	default:
		return jsonEqual(actual, expected)
	}
}

func jsonEqual(a, b any) bool {
	aj, _ := json.Marshal(a)
	bj, _ := json.Marshal(b)
	return string(aj) == string(bj)
}

func unorderedEqual(a, b any) bool {
	aSlice, aOk := toIntSlice(a)
	bSlice, bOk := toIntSlice(b)
	if !aOk || !bOk {
		return jsonEqual(a, b)
	}
	sort.Ints(aSlice)
	sort.Ints(bSlice)
	if len(aSlice) != len(bSlice) {
		return false
	}
	for i := range aSlice {
		if aSlice[i] != bSlice[i] {
			return false
		}
	}
	return true
}

func unorderedNestedEqual(a, b any) bool {
	aMatrix, aOk := toIntMatrix(a)
	bMatrix, bOk := toIntMatrix(b)
	if !aOk || !bOk {
		return jsonEqual(a, b)
	}
	normalize := func(matrix [][]int) []string {
		normalized := make([]string, len(matrix))
		for i := range matrix {
			row := append([]int(nil), matrix[i]...)
			sort.Ints(row)
			rowJSON, _ := json.Marshal(row)
			normalized[i] = string(rowJSON)
		}
		sort.Strings(normalized)
		return normalized
	}
	aNorm := normalize(aMatrix)
	bNorm := normalize(bMatrix)
	if len(aNorm) != len(bNorm) {
		return false
	}
	for i := range aNorm {
		if aNorm[i] != bNorm[i] {
			return false
		}
	}
	return true
}

func toIntSlice(v any) ([]int, bool) {
	switch val := v.(type) {
	case []int:
		return val, true
	case []any:
		result := make([]int, len(val))
		for i, item := range val {
			n, ok := toFloat(item)
			if !ok {
				return nil, false
			}
			result[i] = int(n)
		}
		return result, true
	default:
		return nil, false
	}
}

func toIntMatrix(v any) ([][]int, bool) {
	switch val := v.(type) {
	case [][]int:
		return val, true
	case []any:
		result := make([][]int, len(val))
		for i, item := range val {
			row, ok := toIntSlice(item)
			if !ok {
				return nil, false
			}
			result[i] = row
		}
		return result, true
	default:
		return nil, false
	}
}

func toFloat(v any) (float64, bool) {
	switch val := v.(type) {
	case float64:
		return val, true
	case int:
		return float64(val), true
	case json.Number:
		f, err := val.Float64()
		return f, err == nil
	default:
		return 0, false
	}
}

// ---------------------------------------------------------------------------
// Verdict reporting
// ---------------------------------------------------------------------------

func Truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen-3] + "..."
}

func ReportProgress(passed int, total int) {
	path := os.Getenv("GRINDX_PROGRESS_FILE")
	if path == "" {
		return
	}
	if progressFile == nil {
		file, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0o644)
		if err != nil {
			return
		}
		progressFile = file
	}
	payload := []byte(fmt.Sprintf("%d,%d", passed, total))
	_, _ = progressFile.Seek(0, 0)
	_, _ = progressFile.Write(payload)
	_ = progressFile.Truncate(int64(len(payload)))
}

func ReportAC(total int) {
	out, _ := json.Marshal(map[string]any{
		"verdict": "AC",
		"passed":  total,
		"total":   total,
	})
	fmt.Println(string(out))
	os.Exit(0)
}

func ReportWA(caseIdx int, input, expected, actual any, total int, category string) {
	inputJSON, _ := json.Marshal(input)
	expectedJSON, _ := json.Marshal(expected)
	actualJSON, _ := json.Marshal(actual)
	out, _ := json.Marshal(map[string]any{
		"verdict":          "WA",
		"failed_case":      caseIdx,
		"input_preview":    Truncate(string(inputJSON), 200),
		"expected_preview": Truncate(string(expectedJSON), 200),
		"actual_preview":   Truncate(string(actualJSON), 200),
		"passed":           caseIdx,
		"total":            total,
		"category":         category,
	})
	fmt.Println(string(out))
	os.Exit(1)
}
