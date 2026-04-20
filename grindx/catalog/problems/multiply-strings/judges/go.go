        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("multiply-strings")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var num1 string
	var num2 string
	_ = json.Unmarshal(c.Input[0], &num1)
	_ = json.Unmarshal(c.Input[1], &num2)
	actual := multiply(num1, num2)
	var expected string
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, []any{num1, num2}, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
