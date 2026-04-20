package main

import (
	"encoding/json"
	"sort"
)

func generateLargeCases() []TestCase {
	descending := make([]int, 50000)
	descendingExpected := make([]int, 50000)
	for i := 0; i < 50000; i++ {
		descending[i] = 50000 - i
		descendingExpected[i] = i + 1
	}

	mixed := make([]int, 50000)
	for i := 0; i < 50000; i++ {
		mixed[i] = ((i * 8191) % 200001) - 100000
	}
	mixedExpected := append([]int(nil), mixed...)
	sort.Ints(mixedExpected)

	duplicates := make([]int, 50000)
	for i := 0; i < 50000; i++ {
		duplicates[i] = ((i * 37) % 31) - 15
	}
	duplicatesExpected := append([]int(nil), duplicates...)
	sort.Ints(duplicatesExpected)

	marshal := func(values []int) json.RawMessage {
		b, _ := json.Marshal(values)
		return b
	}

	return []TestCase{
		{
			Input:    []json.RawMessage{marshal(descending)},
			Expected: marshal(descendingExpected),
			Category: "stress",
		},
		{
			Input:    []json.RawMessage{marshal(mixed)},
			Expected: marshal(mixedExpected),
			Category: "stress",
		},
		{
			Input:    []json.RawMessage{marshal(duplicates)},
			Expected: marshal(duplicatesExpected),
			Category: "stress",
		},
	}
}

func main() {
	tc := LoadCases("sort-list")
	cases := append(tc.Cases, generateLargeCases()...)
	total := len(cases)
	for idx, c := range cases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)
		actual := LinkedListToList(sortList(ListToLinkedList(arr)))
		var expected []int
		json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
