        package main

        import (
	"encoding/json"
)

                        func rowsToBytes(rows []string) [][]byte {
	out := make([][]byte, len(rows))
	for i, row := range rows {
		out[i] = []byte(row)
	}
	return out
                }


        func main() {
	tc := LoadCases("maximal-rectangle")
	total := len(tc.Cases)
        for i, c := range tc.Cases {
	var rows []string
	_ = json.Unmarshal(c.Input[0], &rows)
	actual := maximalRectangle(rowsToBytes(rows))
	var expected int
	_ = json.Unmarshal(c.Expected, &expected)
	if actual != expected {
		ReportWA(i, rows, expected, actual, total, c.Category)
	}
	ReportProgress(i + 1, total)
}

	ReportAC(total)
        }
