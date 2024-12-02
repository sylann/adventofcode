package year_2024

import (
	"fmt"
	"strconv"
	"strings"
)

type Day02 struct{}

func init() {
	Solutions[02] = Day02{}
}

func parseLevels(report string) []int64 {
	levelsRaw := strings.Split(report, " ")
	levels := make([]int64, 0)
	for _, l := range levelsRaw {
		n, _ := strconv.ParseInt(l, 10, 64)
		levels = append(levels, n)
	}
	return levels
}

// reportIsSafe returns whether a report is safe.
// A report is considered safe if:
// 1. levels are either all increasing or all decreasing
// 2. distance between adjacent levels is >= 1 and <= 3
func reportIsSafe(report []int64) bool {
	decreasing := report[0] > report[1]
	for i := 1; i < len(report); i++ {
		a, b := report[i-1], report[i]
		diff := b - a
		if decreasing {
			diff = -diff
		}
		if diff < 1 || diff > 3 {
			return false
		}
	}
	return true
}

// makeAdjustedReport produces a new slice from the given report where skipIdx is omitted.
func makeAdjustedReport(report []int64, skipIdx int) []int64 {
	adjusted := make([]int64, 0)
	for i, level := range report {
		if i != skipIdx {
			adjusted = append(adjusted, level)
		}
	}
	return adjusted
}

// reportIsAlmostSafe returns whether a report is safe or would be safe by removing 1 level from it.
func reportIsAlmostSafe(report []int64) bool {
	if reportIsSafe(report) {
		return true
	}

	// find if we can remove 1 level and make the report safe
	for i := 0; i < len(report); i++ {
		adjusted := makeAdjustedReport(report, i)
		if reportIsSafe(adjusted) {
			return true
		}
	}
	return false
}

func (Day02) Solve1(data string) string {
	trimed := strings.TrimSpace(data)
	reports := strings.Split(trimed, "\n")
	total := 0
	for _, report := range reports {
		levels := parseLevels(report)
		if reportIsSafe(levels) {
			total++
		}
	}
	return fmt.Sprintf("%d", total)
}

func (Day02) Solve2(data string) string {
	trimed := strings.TrimSpace(data)
	reports := strings.Split(trimed, "\n")
	total := 0
	for _, report := range reports {
		levels := parseLevels(report)
		if reportIsAlmostSafe(levels) {
			total++
		}
	}
	return fmt.Sprintf("%d", total)
}
