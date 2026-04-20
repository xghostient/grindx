        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("assign-cookies")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var arr1, arr2 []int
	_ = json.Unmarshal(c.Input[0], &arr1)
	_ = json.Unmarshal(c.Input[1], &arr2)
	actual := findContentChildren(append([]int(nil), arr1...), append([]int(nil), arr2...))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{arr1, arr2}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
