        package main

        import "encoding/json"

        func main() {
	tc := LoadCases("disjoint-set-implementation")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var n int
		_ = json.Unmarshal(c.Input[0], &n)
		dsu := NewDSU(n)
		var expected []bool
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var args []int
			_ = json.Unmarshal(c.OpInputs[j], &args)
			var actual bool
			if op == "union" {
				actual = dsu.Union(args[0], args[1])
			} else {
				actual = dsu.Find(args[0]) == dsu.Find(args[1])
			}
			if actual != expected[j] {
				ReportWA(i, []any{op, args}, expected[j], actual, total, c.Category)
			}
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
        }
