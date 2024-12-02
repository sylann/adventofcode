package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

func BenchmarkDay02_Solve1(b *testing.B) {
	day, data := Day02{}, utils.ReadInputData(b, "year_2024/day_02.txt")
	for i := 0; i < b.N; i++ {
		day.Solve1(data)
	}
}

func BenchmarkDay02_Solve2(b *testing.B) {
	day, data := Day02{}, utils.ReadInputData(b, "year_2024/day_02.txt")
	for i := 0; i < b.N; i++ {
		day.Solve2(data)
	}
}
