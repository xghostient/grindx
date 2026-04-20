        package main

        import (
	"encoding/json"
)



        func main() {
	tc := LoadCases("evaluate-reverse-polish-notation")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var rows []string
	_ = json.Unmarshal(c.Input[0], &rows)
	actual := evalRPN(append([]string(nil), rows...))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, rows, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
