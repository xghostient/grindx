        package main

        import (
	"encoding/json"
	"reflect"
)



        func main() {
	tc := LoadCases("reverse-stack")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var stack []int
	_ = json.Unmarshal(c.Input[0], &stack)
	reverseStack(&stack)
	var expected []int
	_ = json.Unmarshal(c.Expected, &expected)
	if !reflect.DeepEqual(stack, expected) {
		ReportWA(i, c.Input[0], expected, stack, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
