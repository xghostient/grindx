package main

import "encoding/json"

func generateLargeCases() []TestCase {
	stressOne := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressOne[i] = i + 2
	}
	for i := 24999; i < 50000; i++ {
		stressOne[i] = 1
	}

	stressTwo := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressTwo[i] = -(i + 2)
	}
	for i := 24999; i < 50000; i++ {
		stressTwo[i] = -1
	}

	stressThree := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressThree[i] = 1000000000 - i
	}
	for i := 24999; i < 50000; i++ {
		stressThree[i] = 999999999
	}

	stressFour := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressFour[i] = -(1000000000 - i)
	}
	for i := 24999; i < 50000; i++ {
		stressFour[i] = -999999999
	}

	stressFive := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressFive[i] = 500000000 + i
	}
	for i := 24999; i < 50000; i++ {
		stressFive[i] = 7
	}

	stressSix := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressSix[i] = -(500000000 + i)
	}
	for i := 24999; i < 50000; i++ {
		stressSix[i] = -7
	}

	stressSeven := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressSeven[i] = 250000000 + i
	}
	for i := 24999; i < 50000; i++ {
		stressSeven[i] = 123456789
	}

	stressEight := make([]int, 50000)
	for i := 0; i < 24999; i++ {
		stressEight[i] = -(250000000 + i)
	}
	for i := 24999; i < 50000; i++ {
		stressEight[i] = -123456789
	}

	marshal := func(v any) json.RawMessage {
		b, _ := json.Marshal(v)
		return b
	}
	base := []TestCase{
		{Input: []json.RawMessage{marshal(stressOne)}, Expected: marshal(1), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressTwo)}, Expected: marshal(-1), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressThree)}, Expected: marshal(999999999), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressFour)}, Expected: marshal(-999999999), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressFive)}, Expected: marshal(7), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressSix)}, Expected: marshal(-7), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressSeven)}, Expected: marshal(123456789), Category: "stress"},
		{Input: []json.RawMessage{marshal(stressEight)}, Expected: marshal(-123456789), Category: "stress"},
	}
	out := make([]TestCase, 0, len(base)*4)
	for rep := 0; rep < 4; rep++ {
		out = append(out, base...)
	}
	return out
}

func main() {
	tc := LoadCases("majority-element")
	cases := append(tc.Cases, generateLargeCases()...)
	total := len(cases)
	for i, c := range cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var expected int
		json.Unmarshal(c.Expected, &expected)

		result := majorityElement(arg0Input)

		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
}
