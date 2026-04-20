        package main

        import (
	"encoding/json"
	"reflect"
        )

        func main() {
	tc := LoadCases("implement-trie-prefix-tree")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		obj := Constructor()
		var expected []json.RawMessage
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var rawArgs []string
			_ = json.Unmarshal(c.OpInputs[j], &rawArgs)
			stringArg := ""
			if len(rawArgs) > 0 {
				stringArg = rawArgs[0]
			}
			var actual any
			var want any
			if op == "insert" {
				obj.Insert(stringArg)
				actual = nil
				want = nil
			}
			if op == "search" {
				actual = obj.Search(stringArg)
				var tmp bool
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if op == "startsWith" {
				actual = obj.StartsWith(stringArg)
				var tmp bool
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if !reflect.DeepEqual(actual, want) {
				ReportWA(i, []any{op, rawArgs}, want, actual, total, c.Category)
			}
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
        }
