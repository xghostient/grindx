        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("car-fleet")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var target int
	var position []int
	var speed []int
	_ = json.Unmarshal(c.Input[0], &target)
	_ = json.Unmarshal(c.Input[1], &position)
	_ = json.Unmarshal(c.Input[2], &speed)
	actual := carFleet(target, append([]int(nil), position...), append([]int(nil), speed...))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{target, position, speed}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
