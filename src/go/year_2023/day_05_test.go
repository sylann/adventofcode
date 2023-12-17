package year_2023

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

func BenchmarkDay05_Solve1(b *testing.B) {
	day, data := Day05{}, utils.ReadInputData(b, "year_2023/day_05.txt")
	for i := 0; i < b.N; i++ {
		day.Solve1(data)
	}
}

func BenchmarkDay05_Solve2(b *testing.B) {
	day, data := Day05{}, utils.ReadInputData(b, "year_2023/day_05.txt")
	for i := 0; i < b.N; i++ {
		day.Solve2(data)
	}
}
