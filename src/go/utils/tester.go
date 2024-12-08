package utils

import (
	"fmt"
	"os"
	"strings"
	"testing"
)

// ReadInputData tries to read a file at `../../../inputs/<name>`.
// If the file exists, it returns the file's content as is.
// Otherwise, the test is immediately skipped.
func ReadInputData(tb testing.TB, name string) string {
	path := fmt.Sprintf("../../../inputs/%s", name)
	bytes, err := os.ReadFile(path)
	if err != nil {
		tb.Skip(err)
	}
	return string(bytes)
}

// ReadOutputData tries to read a file at `../../../outputs/<name>`.
// If the file exists, it returns the file's content trimmed of whitespaces.
// Otherwise, the test is immediately skipped.
func ReadOutputData(tb testing.TB, name string) string {
	path := fmt.Sprintf("../../../outputs/%s", name)
	bytes, err := os.ReadFile(path)
	if err != nil {
		tb.Skip(err)
	}
	return strings.TrimSpace(string(bytes))
}

// GetData is a shortcut for calling both ReadInputData and ReadOutputData.
func GetData(tb testing.TB, year, day, part int, suffix string) (data string, want string) {
	data = ReadInputData(tb, fmt.Sprintf("year_%d/day_%02d%s.txt", year, day, suffix))
	want = ReadOutputData(tb, fmt.Sprintf("year_%d/day_%02d_%d%s.txt", year, day, part, suffix))
	return data, want
}
