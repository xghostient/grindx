package main

import (
	"encoding/json"
	"sort"
)

func generateLargeCases() []struct {
	nums            []int
	target          int
	expectedIndices []int
} {
	const n = 10000
	cases := make([]struct {
		nums            []int
		target          int
		expectedIndices []int
	}, 0, 4)

	nums := make([]int, n)
	nums[0] = -500000000
	for i := 1; i < n-1; i++ {
		nums[i] = 200000000 + ((i * 7919) % 700000000)
	}
	nums[n-1] = 123456789
	cases = append(cases, struct {
		nums            []int
		target          int
		expectedIndices []int
	}{nums: nums, target: -376543211, expectedIndices: []int{0, n - 1}})

	nums = make([]int, n)
	for i := 0; i < n; i++ {
		nums[i] = 300000000 + ((i * 1237) % 600000000)
	}
	dupI, dupJ := 137, 9862
	nums[dupI] = 123456789
	nums[dupJ] = 123456789
	cases = append(cases, struct {
		nums            []int
		target          int
		expectedIndices []int
	}{nums: nums, target: 246913578, expectedIndices: []int{dupI, dupJ}})

	nums = make([]int, n)
	for i := 0; i < n; i++ {
		nums[i] = 1 + ((i * 48271) % 999999998)
	}
	lowI, highI := 4000, 7000
	nums[lowI] = -1000000000
	nums[highI] = 1000000000
	cases = append(cases, struct {
		nums            []int
		target          int
		expectedIndices []int
	}{nums: nums, target: 0, expectedIndices: []int{lowI, highI}})

	nums = make([]int, n)
	for i := 0; i < n; i++ {
		nums[i] = 1 + ((i * 8191) % 999999999)
	}
	zeroI, zeroJ := 2500, 7500
	nums[zeroI] = 0
	nums[zeroJ] = 0
	cases = append(cases, struct {
		nums            []int
		target          int
		expectedIndices []int
	}{nums: nums, target: 0, expectedIndices: []int{zeroI, zeroJ}})

	return cases
}

func validIndexPair(result []int, size int) bool {
	if len(result) != 2 {
		return false
	}
	for _, idx := range result {
		if idx < 0 || idx >= size {
			return false
		}
	}
	return true
}

func main() {
	tc := LoadCases("two-sum")
	basicCases := tc.Cases

	largeCases := generateLargeCases()

	total := len(basicCases) + len(largeCases)

	// Run basic cases
	for i, c := range basicCases {
		var nums []int
		json.Unmarshal(c.Input[0], &nums)
		var target int
		json.Unmarshal(c.Input[1], &target)

		numsCopy := make([]int, len(nums))
		copy(numsCopy, nums)
		result := twoSum(numsCopy, target)

		var expected []int
		json.Unmarshal(c.Expected, &expected)

		if !validIndexPair(result, len(nums)) {
			ReportWA(i, c.Input, expected, result, total, c.Category)
		}

		sortedResult := make([]int, len(result))
		copy(sortedResult, result)
		sort.Ints(sortedResult)

		sortedExpected := make([]int, len(expected))
		copy(sortedExpected, expected)
		sort.Ints(sortedExpected)

		match := len(sortedResult) == len(sortedExpected)
		if match {
			for k := range sortedResult {
				if sortedResult[k] != sortedExpected[k] {
					match = false
					break
				}
			}
		}
		if !match {
			ReportWA(i, c.Input, expected, result, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	// Run large cases
	for li, lc := range largeCases {
		idx := len(basicCases) + li
		numsCopy := make([]int, len(lc.nums))
		copy(numsCopy, lc.nums)
		result := twoSum(numsCopy, lc.target)

		if !validIndexPair(result, len(lc.nums)) {
			ReportWA(idx, "large input", lc.expectedIndices, result, total, "tle")
		}

		sortedResult := make([]int, len(result))
		copy(sortedResult, result)
		sort.Ints(sortedResult)
		sortedExpected := make([]int, len(lc.expectedIndices))
		copy(sortedExpected, lc.expectedIndices)
		sort.Ints(sortedExpected)

		match := true
		for i := range sortedResult {
			if sortedResult[i] != sortedExpected[i] {
				match = false
				break
			}
		}
		if !match {
			ReportWA(idx, "large input", lc.target, result, total, "tle")
		}
	}

	ReportAC(total)
}
