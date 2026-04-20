        package main

        import (
	"encoding/json"
)

        func main() {
	tc := LoadCases("count-primes")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var n int
	_ = json.Unmarshal(c.Input[0], &n)
	actual := countPrimes(n)
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, n, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
