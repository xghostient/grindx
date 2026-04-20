package main

import "encoding/json"

func main() {
	tc := LoadCases("palindrome-linked-list")
	total := len(tc.Cases)
	for idx, c := range tc.Cases {
		var arr []int
		json.Unmarshal(c.Input[0], &arr)
		actual := isPalindrome(ListToLinkedList(arr))
		var expected bool
		json.Unmarshal(c.Expected, &expected)
		if actual != expected {
			ReportWA(idx, c.Input, expected, actual, total, c.Category)
		}
		ReportProgress(idx + 1, total)
	}
	ReportAC(total)
}
