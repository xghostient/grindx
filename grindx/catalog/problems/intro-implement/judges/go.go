        package main

        import (
	"encoding/json"
	"reflect"
        )

        func main() {
	tc := LoadCases("intro-implement")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		obj := NewMinHeap()
		var expected []json.RawMessage
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var args []int
			_ = json.Unmarshal(c.OpInputs[j], &args)
			var actual any
			var want any
			if op == "insert" {
				obj.Insert(args[0])
				actual = nil
				want = nil
			}
			if op == "extractMin" {
				actual = obj.ExtractMin()
				var tmp int
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if op == "peek" {
				actual = obj.Peek()
				var tmp int
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if op == "size" {
				actual = obj.Size()
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
