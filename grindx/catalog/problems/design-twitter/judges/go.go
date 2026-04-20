        package main

        import (
	"encoding/json"
	"reflect"
        )

        func main() {
	tc := LoadCases("design-twitter")
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
			if op == "postTweet" {
				obj.PostTweet(args[0], args[1])
				actual = nil
				want = nil
			}
			if op == "getNewsFeed" {
				actual = obj.GetNewsFeed(args[0])
				var tmp []int
				_ = json.Unmarshal(expected[j], &tmp)
				want = tmp
			}
			if op == "follow" {
				obj.Follow(args[0], args[1])
				actual = nil
				want = nil
			}
			if op == "unfollow" {
				obj.Unfollow(args[0], args[1])
				actual = nil
				want = nil
			}
			if !reflect.DeepEqual(actual, want) {
				ReportWA(i, []any{op, args}, want, actual, total, c.Category)
			}
		}
		ReportProgress(i + 1, total)
	}
	ReportAC(total)
        }
