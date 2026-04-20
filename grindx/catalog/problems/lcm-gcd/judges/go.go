        package main

        import (
	"encoding/json"
	"reflect"
)

        func main() {
	tc := LoadCases("lcm-gcd")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var a, b int
	_ = json.Unmarshal(c.Input[0], &a)
	_ = json.Unmarshal(c.Input[1], &b)
	actual := lcmAndGcd(a, b)
	var expected []int64
	_ = json.Unmarshal(c.Expected, &expected)
	if actual == nil {
		actual = []int64{}
	}
	if !reflect.DeepEqual(actual, expected) {
		ReportWA(i, []int{a, b}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
