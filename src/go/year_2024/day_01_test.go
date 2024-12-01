package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

func BenchmarkDay01_Solve1(b *testing.B) {
	day, data := Day01{}, utils.ReadInputData(b, "year_2024/day_01.txt")
	for i := 0; i < b.N; i++ {
		day.Solve1(data)
	}
}

func BenchmarkDay01_Solve2(b *testing.B) {
	day, data := Day01{}, utils.ReadInputData(b, "year_2024/day_01.txt")
	for i := 0; i < b.N; i++ {
		day.Solve2(data)
	}
}
