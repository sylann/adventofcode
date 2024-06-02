package year_2023

import (
	"fmt"
	"strings"
)

type Day01 struct{}

func init() {
	Solutions[01] = Day01{}
}

var spelledDigits = []string{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}

func findDigit(line string, reversed bool, checkSpelledDigits bool) int {
	for i := range line {
		if reversed {
			i = len(line) - 1 - i
		}
		chr := line[i]
		if '0' <= chr && chr <= '9' {
			return int(chr - '0')
		}
		if checkSpelledDigits {
			for iSpelling, spelling := range spelledDigits {
				found := false
				if !reversed {
					found = strings.HasPrefix(line[i:], spelling)
				} else {
					found = strings.HasSuffix(line[:i+1], spelling)
				}
				if found {
					return iSpelling + 1
				}
			}
		}
	}
	return 0
}

func sumDigits(data string, checkSpelledDigits bool) int {
	out := 0
	for _, line := range strings.Split(data, "\n") {
		first := findDigit(line, false, checkSpelledDigits)
		last := findDigit(line, true, checkSpelledDigits)
		out += first*10 + last
	}
	return out
}

func (Day01) Solve1(data string) string {
	return fmt.Sprintf("%d", sumDigits(data, false))
}

func (Day01) Solve2(data string) string {
	return fmt.Sprintf("%d", sumDigits(data, true))
}
