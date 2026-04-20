package main

import "encoding/json"

func buildLargeCase(n int, missing int, repeating int) TestCase {
	arr := make([]int, n)
	for i := range arr {
		arr[i] = i + 1
	}
	arr[missing-1] = repeating
	marshal := func(v any) json.RawMessage {
		b, _ := json.Marshal(v)
		return b
	}
	return TestCase{
		Input:    []json.RawMessage{marshal(arr)},
		Expected: marshal([]int{repeating, missing}),
		Category: "stress",
	}
}

func generateLargeCases() []TestCase {
	const n = 100000
	return []TestCase{
		buildLargeCase(n, 1, n),
		buildLargeCase(n, n, n/2),
		buildLargeCase(n, 42424, 99999),
	}
}

func main() {
	tc := LoadCases("missing-repeating")
	cases := append(tc.Cases, generateLargeCases()...)
	total := len(cases)
	for i, c := range cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var expected []int
		json.Unmarshal(c.Expected, &expected)

		result := findMissingRepeating(arg0Input)
		if result == nil {
			result = []int{}
		}
		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
