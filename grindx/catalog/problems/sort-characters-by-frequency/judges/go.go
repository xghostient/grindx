        package main

        import (
	"encoding/json"
)

        func isValidFrequencySort(source string, actual string) bool {
if len(source) != len(actual) {
	return false
}
counts := map[byte]int{}
seen := map[byte]int{}
for i := 0; i < len(source); i++ {
	counts[source[i]]++
}
for i := 0; i < len(actual); i++ {
	seen[actual[i]]++
}
if len(counts) != len(seen) {
	return false
}
for ch, count := range counts {
	if seen[ch] != count {
		return false
	}
}
for i := 1; i < len(actual); i++ {
	if counts[actual[i-1]] < counts[actual[i]] {
		return false
	}
}
return true
}


        func main() {
	tc := LoadCases("sort-characters-by-frequency")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	_ = json.Unmarshal(c.Input[0], &s)
	actual := frequencySort(s)
	if !isValidFrequencySort(s, actual) {
		ReportWA(i, s, "valid frequency-sorted string", actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
