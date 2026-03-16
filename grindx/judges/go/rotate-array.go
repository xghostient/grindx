package main

import (
	"encoding/json"
	"math/rand"
)

func main() {
	tc := LoadCases("rotate-array")
	basicCases := tc.Cases

	// Generate large cases for TLE detection
	type largeCase struct {
		nums []int
		k    int
	}
	rng := rand.New(rand.NewSource(42))
	var largeCases []largeCase
	for _, n := range []int{100000} {
		nums := make([]int, n)
		for i := 0; i < n; i++ {
			nums[i] = rng.Intn(2000000001) - 1000000000
		}
		k := rng.Intn(n) + 1
		largeCases = append(largeCases, largeCase{nums: nums, k: k})
	}

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
	}

	// Run large cases
	for li, lc := range largeCases {
		idx := len(basicCases) + li
		numsCopy := make([]int, len(lc.nums))
		copy(numsCopy, lc.nums)
		rotate(numsCopy, lc.k)

		// Compute expected by reference rotation
		n := len(lc.nums)
		effK := lc.k % n
		expected := make([]int, n)
		for i := 0; i < n; i++ {
			expected[(i+effK)%n] = lc.nums[i]
		}

		if !Compare(numsCopy, expected, "exact") {
			ReportWA(idx, "large input (100K elements)", expected, numsCopy, total, "tle")
		}
	}

	ReportAC(total)
}
