        package main

        import (
	"encoding/json"
)

var isBadVersion func(int) bool

        func main() {
        	tc := LoadCases("first-bad-version")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var pair []int
	_ = json.Unmarshal(c.Input[0], &pair)
	n, bad := pair[0], pair[1]
	isBadVersion = func(version int) bool {
		return version >= bad
	}
	actual := firstBadVersion(n)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, pair, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
