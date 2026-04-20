package main

import "encoding/json"

type largeCase struct {
	n        int
	unions   [][]int
	queries  [][]int
	expected []bool
}

func generateLargeCases() []largeCase {
	cases := make([]largeCase, 0, 4)
	for variant := 0; variant < 4; variant++ {
		n := 100000
		unions := make([][]int, n-1)
		for i := 0; i < n-1; i++ {
			unions[i] = []int{i, i + 1}
		}
		var queries [][]int
		switch variant {
		case 0:
			queries = make([][]int, 100000)
			for i := range queries {
				queries[i] = []int{0, n - 1}
			}
		case 1:
			queries = make([][]int, 100000)
			for i := 0; i < 100000; i++ {
				queries[i] = []int{0, n - 1 - i}
			}
		case 2:
			queries = make([][]int, 100000)
			for i := 0; i < 100000; i++ {
				queries[i] = []int{i, n - 1}
			}
		default:
			queries = make([][]int, 100000)
			for i := 0; i < 50000; i++ {
				queries[2*i] = []int{0, n / 2}
				queries[2*i+1] = []int{n / 3, n - 1}
			}
		}
		expected := make([]bool, len(queries))
		for i := range expected {
			expected[i] = true
		}
		cases = append(cases, largeCase{n: n, unions: unions, queries: queries, expected: expected})
	}
	return cases
}

func main() {
	tc := LoadCases("union-find")
	largeCases := generateLargeCases()
	total := len(tc.Cases) + len(largeCases)
	for i, c := range tc.Cases {
		var n int
		var unions [][]int
		var queries [][]int
		var expected []bool
		json.Unmarshal(c.Input[0], &n)
		json.Unmarshal(c.Input[1], &unions)
		json.Unmarshal(c.Input[2], &queries)
		json.Unmarshal(c.Expected, &expected)
		uf := NewUnionFind(n)
		for _, pair := range unions {
			uf.Union(pair[0], pair[1])
		}
		actual := make([]bool, len(queries))
		for idx, pair := range queries {
			actual[idx] = uf.Connected(pair[0], pair[1])
		}
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	for li, c := range largeCases {
		uf := NewUnionFind(c.n)
		for _, pair := range c.unions {
			uf.Union(pair[0], pair[1])
		}
		actual := make([]bool, len(c.queries))
		for i, pair := range c.queries {
			actual[i] = uf.Connected(pair[0], pair[1])
		}
		if !Compare(actual, c.expected, "exact") {
			ReportWA(len(tc.Cases)+li, "large input", c.expected, actual, total, "tle")
		}
	}

	ReportAC(total)
}
