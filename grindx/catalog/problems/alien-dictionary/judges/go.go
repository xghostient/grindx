        package main

        import (
	"encoding/json"
	"sort"
	"strings"
        )

        func cloneStringMatrix(matrix [][]string) [][]string {
	result := make([][]string, len(matrix))
	for i := range matrix { result[i] = append([]string(nil), matrix[i]...) }
	return result
}

func normalizePaths(paths [][]string) [][]string {
	result := make([][]string, len(paths))
	for i := range paths { result[i] = append([]string(nil), paths[i]...) }
	sort.Slice(result, func(i, j int) bool {
		return strings.Join(result[i], "") < strings.Join(result[j], "")
	})
	if result == nil { return [][]string{} }
	return result
}

func validateAlienOrder(words []string, order string) bool {
	chars := map[rune]bool{}
	for _, word := range words {
		for _, ch := range word { chars[ch] = true }
	}
	seen := map[rune]bool{}
	rank := map[rune]int{}
	for i, ch := range order {
		if seen[ch] { return false }
		seen[ch] = true
		rank[ch] = i
	}
	if len(seen) != len(chars) { return false }
	for ch := range chars {
		if !seen[ch] { return false }
	}
	for i := 0; i+1 < len(words); i++ {
		a, b := []rune(words[i]), []rune(words[i+1])
		j := 0
		for j < len(a) && j < len(b) && a[j] == b[j] { j++ }
		if j == len(a) || j == len(b) {
			if len(a) > len(b) && j == len(b) { return false }
			continue
		}
		if rank[a[j]] > rank[b[j]] { return false }
	}
	return true
}

        func main() {
	 tc := LoadCases("alien-dictionary")
	 total := len(tc.Cases)
            for i, c := range tc.Cases {
    	var words []string
    	_ = json.Unmarshal(c.Input[0], &words)
    	actual := alienOrder(append([]string(nil), words...))
    	var expected string
    	_ = json.Unmarshal(c.Expected, &expected)
    	if expected == "" {
    		if actual != "" {
    			ReportWA(i, words, expected, actual, total, c.Category)
    		}
    	} else if !validateAlienOrder(words, actual) {
    		ReportWA(i, words, expected, actual, total, c.Category)
    	}
            	ReportProgress(i + 1, total)
    }

	 ReportAC(total)
        }
