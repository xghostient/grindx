        package main

        import (
	"encoding/json"
	"strings"
)

        func isValidMinWindow(source string, target string, expected string, actual string) bool {
if len(actual) != len(expected) {
	return false
}
if expected == "" {
	return actual == ""
}
if !strings.Contains(source, actual) {
	return false
}
need := map[byte]int{}
have := map[byte]int{}
for i := 0; i < len(target); i++ {
	need[target[i]]++
}
for i := 0; i < len(actual); i++ {
	have[actual[i]]++
}
for ch, count := range need {
	if have[ch] < count {
		return false
	}
}
return true
}


        func main() {
	tc := LoadCases("minimum-window-substring")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s, t string
	_ = json.Unmarshal(c.Input[0], &s)
	_ = json.Unmarshal(c.Input[1], &t)
	actual := minWindow(s, t)
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if !isValidMinWindow(s, t, expected, actual) {
		ReportWA(i, []any{s, t}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
