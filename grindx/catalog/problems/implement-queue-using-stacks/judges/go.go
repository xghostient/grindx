            package main

            import (
	"encoding/json"
	"reflect"
            )

            func main() {
	tc := LoadCases("implement-queue-using-stacks")
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
			if op == "push" {
				obj.Push(args[0])
				actual = nil
				want = nil
			}

			if op == "pop" {
				actual = obj.Pop()
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

			if op == "empty" {
				actual = obj.Empty()
				var tmp bool
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
