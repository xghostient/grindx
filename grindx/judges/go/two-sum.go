package main

import (
	"encoding/json"
	"math/rand"
	"sort"
)

func main() {
	tc := LoadCases("two-sum")
	basicCases := tc.Cases

	// Generate large cases for TLE detection
	type largeCase struct {
		nums   []int
		target int
	}
	rng := rand.New(rand.NewSource(42))
	var largeCases []largeCase
	for _, n := range []int{10000, 100000} {
		nums := make([]int, n)
		for k := 0; k < n; k++ {
			nums[k] = rng.Intn(2000000001) - 1000000000
		}
		i := rng.Intn(n)
		j := rng.Intn(n)
		for j == i {
			j = (j + 1) % n
		}
		target := nums[i] + nums[j]
		largeCases = append(largeCases, largeCase{nums: nums, target: target})
	}

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
	}

	// Run large cases
	for li, lc := range largeCases {
		idx := len(basicCases) + li
		numsCopy := make([]int, len(lc.nums))
		copy(numsCopy, lc.nums)
		result := twoSum(numsCopy, lc.target)

		if len(result) != 2 || result[0] == result[1] ||
			lc.nums[result[0]]+lc.nums[result[1]] != lc.target {
			ReportWA(idx, "large input", lc.target, result, total, "tle")
		}
	}

	ReportAC(total)
}
