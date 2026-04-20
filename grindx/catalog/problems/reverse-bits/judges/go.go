        package main

        import (
	"encoding/json"
)

        func main() {
        	tc := LoadCases("reverse-bits")
        	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var x uint32
	_ = json.Unmarshal(c.Input[0], &x)
	actual := reverseBits(x)
	var expected uint32
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, x, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}
        	ReportAC(total)
        }
