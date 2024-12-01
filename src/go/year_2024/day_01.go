package year_2024

import (
	"fmt"
	"math"
	"slices"
	"strconv"
	"strings"
)

type Day01 struct{}

func init() {
	Solutions[01] = Day01{}
}

func (Day01) Solve1(data string) string {
	trimed := strings.TrimSpace(data)
	lines := strings.Split(trimed, "\n")
	n := len(lines)
	aList := make([]int64, n)
	bList := make([]int64, n)
	for i, line := range lines {
		parts := strings.Split(line, "   ")
		a, b := parts[0], parts[1]
		aList[i], _ = strconv.ParseInt(a, 10, 64)
		bList[i], _ = strconv.ParseInt(b, 10, 64)
	}
	slices.Sort(aList)
	slices.Sort(bList)
	total := 0
	for i := 0; i < n; i++ {
		total += int(math.Abs(float64(aList[i] - bList[i])))
	}
	return fmt.Sprintf("%d\n", total)
}

func (Day01) Solve2(data string) string {
	trimed := strings.TrimSpace(data)
	lines := strings.Split(trimed, "\n")
	n := len(lines)
	aList := make([]int64, n)
	bDict := make(map[int64]int64, n)
	for i, line := range lines {
		parts := strings.Split(line, "   ")
		aList[i], _ = strconv.ParseInt(parts[0], 10, 64)
		b, _ := strconv.ParseInt(parts[1], 10, 64)
		bDict[b]++
	}
	
	var total int64 = 0
	for i := 0; i < n; i++ {
		x := aList[i]
		total += x * bDict[x]
	}
	return fmt.Sprintf("%d\n", total)
}
