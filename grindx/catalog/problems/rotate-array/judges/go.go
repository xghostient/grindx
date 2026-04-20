package main

import (
	"encoding/json"
)

func generateLargeRotateCases() []struct {
	nums     []int
	k        int
	expected []int
} {
	cases := make([]struct {
		nums     []int
		k        int
		expected []int
	}, 0, 8)

	for _, spec := range []struct {
		n     int
		k     int
		start int
		step  int
	}{
		{n: 100000, k: 99999, start: -1000000000, step: 37},
		{n: 100000, k: 87500, start: -999900000, step: 53},
		{n: 100000, k: 75000, start: -999800000, step: 61},
		{n: 100000, k: 62500, start: -999700000, step: 73},
		{n: 100000, k: 50000, start: -999600000, step: 79},
		{n: 100000, k: 37500, start: -999500000, step: 83},
		{n: 100000, k: 25000, start: -999400000, step: 89},
		{n: 99999, k: 99998, start: -999300000, step: 97},
	} {
		nums := make([]int, spec.n)
		for i := 0; i < spec.n; i++ {
			nums[i] = spec.start + (i * spec.step)
		}
		effK := spec.k % spec.n
		expected := make([]int, spec.n)
		if effK == 0 {
			copy(expected, nums)
		} else {
			copy(expected[:effK], nums[spec.n-effK:])
			copy(expected[effK:], nums[:spec.n-effK])
		}
		cases = append(cases, struct {
			nums     []int
			k        int
			expected []int
		}{nums: nums, k: spec.k, expected: expected})
	}

	return cases
}

func main() {
	tc := LoadCases("rotate-array")
	basicCases := tc.Cases

	largeCases := generateLargeRotateCases()

	total := len(basicCases) + len(largeCases)

	// Run basic cases
	for i, c := range basicCases {
		var nums []int
		json.Unmarshal(c.Input[0], &nums)
		var k int
		json.Unmarshal(c.Input[1], &k)

		numsCopy := make([]int, len(nums))
		copy(numsCopy, nums)
		rotate(numsCopy, k)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !Compare(numsCopy, expected, "exact") {
			ReportWA(i, c.Input, expected, numsCopy, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	// Run large cases
	for li, lc := range largeCases {
		idx := len(basicCases) + li
		numsCopy := make([]int, len(lc.nums))
		copy(numsCopy, lc.nums)
		rotate(numsCopy, lc.k)

		if !Compare(numsCopy, lc.expected, "exact") {
			ReportWA(idx, "large input", lc.expected, numsCopy, total, "tle")
		}
	}

	ReportAC(total)
}
