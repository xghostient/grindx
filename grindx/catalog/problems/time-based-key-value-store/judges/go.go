package main

import (
	"encoding/json"
	"reflect"
)

func main() {
	tc := LoadCases("time-based-key-value-store")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		obj := Constructor()
		var expected []json.RawMessage
		_ = json.Unmarshal(c.Expected, &expected)
		for j, op := range c.Operations {
			var actual any
			var want any
			if op == "TimeMap" {
				actual = nil
				want = nil
			} else if op == "set" {
				var args []json.RawMessage
				_ = json.Unmarshal(c.OpInputs[j], &args)
				var key, value string
				var ts int
				_ = json.Unmarshal(args[0], &key)
				_ = json.Unmarshal(args[1], &value)
				_ = json.Unmarshal(args[2], &ts)
				obj.Set(key, value, ts)
				actual = nil
				want = nil
			} else if op == "get" {
				var args []json.RawMessage
				_ = json.Unmarshal(c.OpInputs[j], &args)
				var key string
				var ts int
				_ = json.Unmarshal(args[0], &key)
				_ = json.Unmarshal(args[1], &ts)
				actual = obj.Get(key, ts)
				var tmp string
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if !reflect.DeepEqual(actual, want) {
				ReportWA(i, []any{op}, want, actual, total, c.Category)
			}
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
}
