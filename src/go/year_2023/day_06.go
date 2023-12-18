package year_2023

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

// Get the index of the first instance of c in s, or len(s) if c is not present in s.
func indexByteOrEnd(s string, c byte) int {
	i := strings.IndexByte(s, c)
	if i == -1 {
		i = len(s)
	}
	return i
}

// Read the first occuring number in data (from offset), ignoring spaces between digits.
func parseBadKerning(data string, offset int) (int, int) {
	var i, end, pow, num int

	end = offset + indexByteOrEnd(data[offset:], '\n')
	// fmt.Fprintf(os.Stderr, "loop i: %d..%d\n", offset, end)
	for i = end - 1; i >= offset; i-- {
		// fmt.Fprintf(os.Stderr, "  i=%d -> %c\n", i, data[i])
		if data[i] >= '0' && data[i] <= '9' {
			num += int(data[i]-'0') * int(math.Pow10(pow))
			pow += 1
		}
	}
	i++ // revert last decrement
	return num, end + 1
}

// Count possible choices of how long the button must be pressed to win the race.
func CountChoices(maxTime, bestDist int) int {
	// NOTE: speed <=> time and maxSpeed <=> maxTime because acceleration is 1
	var speed, nChoices int
	for speed < maxTime {
		if speed*(maxTime-speed) > bestDist {
			nChoices++
		}
		speed++
	}
	return nChoices
}

type Day06 struct{}

func init() {
	Solutions[06] = Day06{}
}

func (Day06) Solve1(data string) string {
	fields := strings.Fields(data)
	half := len(fields) / 2
	total := 1
	for i := 1; i < half; i++ {
		time, _ := strconv.Atoi(fields[i])
		dist, _ := strconv.Atoi(fields[i+half])
		total *= CountChoices(time, dist)
	}
	return fmt.Sprint(total)
}

// NOTE: I love how Part II of Advent of Code always manages to surprise you
// in an unexpected way.
func (Day06) Solve2(data string) string {
	maxTime, consumed := parseBadKerning(data, 0)
	bestDist, _ := parseBadKerning(data, consumed)
	total := CountChoices(maxTime, bestDist)
	return fmt.Sprint(total)
}
