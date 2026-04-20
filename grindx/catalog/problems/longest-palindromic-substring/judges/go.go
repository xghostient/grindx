        package main

        import (
	"encoding/json"
	"strings"
)

        func isValidLongestPalindrome(source string, expected string, actual string) bool {
if len(actual) != len(expected) || !strings.Contains(source, actual) {
	return false
}
for i, j := 0, len(actual)-1; i < j; i, j = i+1, j-1 {
	if actual[i] != actual[j] {
		return false
	}
}
return true
}


        func main() {
	tc := LoadCases("longest-palindromic-substring")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	_ = json.Unmarshal(c.Input[0], &s)
	actual := longestPalindrome(s)
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if !isValidLongestPalindrome(s, expected, actual) {
		ReportWA(i, s, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
