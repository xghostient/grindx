        package main

        import (
	"encoding/json"
	"sort"
	"strings"
)

        func cloneStringSlice(values []string) []string {
return append([]string(nil), values...)
}

func normalizeStringGroups(groups [][]string) [][]string {
result := make([][]string, len(groups))
for i := range groups {
	result[i] = append([]string(nil), groups[i]...)
	sort.Strings(result[i])
}
sort.Slice(result, func(i, j int) bool {
	return strings.Join(result[i], "\x01") < strings.Join(result[j], "\x01")
})
return result
}

func deriveProbeStrings(strs []string) []string {
result := make([]string, 0, len(strs)+1)
for _, value := range strs {
	result = append(result, value+"#probe")
}
result = append(result, "|probe|")
return result
}


        func main() {
	tc := LoadCases("group-anagrams")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var strs []string
	_ = json.Unmarshal(c.Input[0], &strs)
	actual := normalizeStringGroups(groupAnagrams(cloneStringSlice(strs)))
	var expected [][]string
	_ = json.Unmarshal(c.Expected, &expected)
	expected = normalizeStringGroups(expected)
	if !Compare(actual, expected, "exact") {
		ReportWA(i, strs, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
