        package main

        import (
	"encoding/json"
	"reflect"
        )

        func main() {
	tc := LoadCases("detect-squares")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		obj := Constructor()
		var expected []json.RawMessage
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var args []int
			_ = json.Unmarshal(c.OpInputs[j], &args)
			var actual any
			var want any
			if op == "add" {
				var rawArgs [][]int
				_ = json.Unmarshal(c.OpInputs[j], &rawArgs)
				args := []int{}
				if len(rawArgs) > 0 {
					args = rawArgs[0]
				}
				obj.Add(args)
				actual = nil
				want = nil
			}
			if op == "count" {
				var rawArgs [][]int
				_ = json.Unmarshal(c.OpInputs[j], &rawArgs)
				args := []int{}
				if len(rawArgs) > 0 {
					args = rawArgs[0]
				}
				actual = obj.Count(args)
				var tmp int
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if !reflect.DeepEqual(actual, want) {
				ReportWA(i, []any{op, args}, want, actual, total, c.Category)
			}
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
        }
