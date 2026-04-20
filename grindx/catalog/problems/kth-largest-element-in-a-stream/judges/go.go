        package main

        import (
	"encoding/json"
	"reflect"
        )

        func main() {
	tc := LoadCases("kth-largest-element-in-a-stream")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
var k int
var nums []int
_ = json.Unmarshal(c.Input[0], &k)
_ = json.Unmarshal(c.Input[1], &nums)
obj := Constructor(k, nums)
		var expected []json.RawMessage
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var args []int
			_ = json.Unmarshal(c.OpInputs[j], &args)
			var actual any
			var want any
			if op == "add" {
				actual = obj.Add(args[0])
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
