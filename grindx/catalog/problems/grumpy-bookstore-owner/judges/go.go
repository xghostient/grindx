package main

import "encoding/json"

type largeCase struct {
	customers []int
	grumpy    []int
	minutes   int
	expected  int
}

func expected(customers []int, grumpy []int, minutes int) int {
	base := 0
	for i, c := range customers {
		if grumpy[i] == 0 {
			base += c
		}
	}
	extra := 0
	for i := 0; i < minutes; i++ {
		if grumpy[i] == 1 {
			extra += customers[i]
		}
	}
	best := extra
	for i := minutes; i < len(customers); i++ {
		if grumpy[i] == 1 {
			extra += customers[i]
		}
		if grumpy[i-minutes] == 1 {
			extra -= customers[i-minutes]
		}
		if extra > best {
			best = extra
		}
	}
	return base + best
}

func generateLargeCases() []largeCase {
	n := 20000
	cases := make([]largeCase, 0, 32)
	for shift := 0; shift < 8; shift++ {
		customers := make([]int, n)
		grumpy := make([]int, n)
		for i := 0; i < n; i++ {
			if (i+shift)%2 == 0 {
				customers[i] = 1000
			} else {
				customers[i] = 1
			}
			grumpy[i] = 1
		}
		minutes := n/2 + (shift % 5)
		cases = append(cases, largeCase{customers, grumpy, minutes, expected(customers, grumpy, minutes)})
	}
	for shift := 0; shift < 8; shift++ {
		customers := make([]int, n)
		grumpy := make([]int, n)
		for i := 0; i < n; i++ {
			customers[i] = ((i + shift) % 9) * 111
			if (i+shift)%3 == 0 {
				grumpy[i] = 1
			}
		}
		minutes := n/2 + (shift % 7)
		cases = append(cases, largeCase{customers, grumpy, minutes, expected(customers, grumpy, minutes)})
	}
	for shift := 0; shift < 8; shift++ {
		customers := make([]int, n)
		grumpy := make([]int, n)
		for i := 0; i < n; i++ {
			if (i+shift)%4 < 2 {
				customers[i] = 5
			} else {
				customers[i] = 20
			}
			if (i + shift) % 5 != 0 {
				grumpy[i] = 1
			}
		}
		minutes := n/3 + (shift % 11)
		cases = append(cases, largeCase{customers, grumpy, minutes, expected(customers, grumpy, minutes)})
	}
	for shift := 0; shift < 8; shift++ {
		customers := make([]int, n)
		grumpy := make([]int, n)
		for i := 0; i < n; i++ {
			customers[i] = 997 - ((i + shift) % 11)
			if (i+shift)%2 == 0 {
				grumpy[i] = 1
			}
		}
		minutes := n - 123 - (shift % 17)
		cases = append(cases, largeCase{customers, grumpy, minutes, expected(customers, grumpy, minutes)})
	}
	return cases
}

func main() {
	tc := LoadCases("grumpy-bookstore-owner")
	largeCases := generateLargeCases()
	total := len(tc.Cases) + len(largeCases)
	for i, c := range tc.Cases {
		var arg0 []int
		json.Unmarshal(c.Input[0], &arg0)
		arg0Input := append([]int(nil), arg0...)
		var arg1 []int
		json.Unmarshal(c.Input[1], &arg1)
		arg1Input := append([]int(nil), arg1...)
		var arg2 int
		json.Unmarshal(c.Input[2], &arg2)
		var expected int
		json.Unmarshal(c.Expected, &expected)

		result := maxSatisfied(arg0Input, arg1Input, arg2)

		actual := result
		if !Compare(actual, expected, "exact") {
			ReportWA(i, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	for li, c := range largeCases {
		result := maxSatisfied(append([]int(nil), c.customers...), append([]int(nil), c.grumpy...), c.minutes)
		if !Compare(result, c.expected, "exact") {
			ReportWA(len(tc.Cases)+li, "large input", c.expected, result, total, "tle")
		}
	}

	ReportAC(total)
}
