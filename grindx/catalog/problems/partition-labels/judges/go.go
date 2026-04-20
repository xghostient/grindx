        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
	tc := LoadCases("partition-labels")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var s string
	_ = json.Unmarshal(c.Input[0], &s)
	actual := partitionLabels(s)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual == nil {
		actual = []int{}
	}
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, s, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
