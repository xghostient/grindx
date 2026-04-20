        package main

        import (
	"encoding/json"
	"sort"
	"strings"
        )

        func cloneMatrix(matrix [][]int) [][]int {
	result := make([][]int, len(matrix))
	for i := range matrix {
		result[i] = append([]int(nil), matrix[i]...)
	}
	return result
}

func normalizeAccounts(accounts [][]string) [][]string {
	result := make([][]string, len(accounts))
	for i, account := range accounts {
		if len(account) == 0 {
			result[i] = []string{}
			continue
		}
		name := account[0]
		seen := map[string]struct{}{}
		var emails []string
		for _, email := range account[1:] {
			if _, ok := seen[email]; ok {
				continue
			}
			seen[email] = struct{}{}
			emails = append(emails, email)
		}
		sort.Strings(emails)
		row := append([]string{name}, emails...)
		result[i] = row
	}
	sort.Slice(result, func(i, j int) bool {
		return strings.Join(result[i], "\x00") < strings.Join(result[j], "\x00")
	})
	return result
}


        func main() {
	tc := LoadCases("accounts-merge")
	total := len(tc.Cases)
	for i, c := range tc.Cases {
		var accounts [][]string
		_ = json.Unmarshal(c.Input[0], &accounts)
		actual := normalizeAccounts(accountsMerge(accounts))
		var expected [][]string
		_ = json.Unmarshal(c.Expected, &expected)
		if !Compare(actual, expected, "exact") {
			ReportWA(i, accounts, expected, actual, total, c.Category)
		}
		ReportProgress(i + 1, total)
	}

	ReportAC(total)
        }
