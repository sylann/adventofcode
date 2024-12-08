package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

func TestDay04_Solve1_example(t *testing.T) {
	day, data := Day04{}, utils.ReadInputData(t, "year_2024/day_04_example.txt")
	expected := "18"
	actual := day.Solve1(data)
	if actual != expected {
		t.Fatalf(`Day04.Solve1() = %s, %s, want "", error`, actual, expected)
	}
}

func TestDay04_Solve2_example(t *testing.T) {
	day, data := Day04{}, utils.ReadInputData(t, "year_2024/day_04_example.txt")
	expected := "9"
	actual := day.Solve2(data)
	if actual != expected {
		t.Fatalf(`Day04.Solve2() = %s, %s, want "", error`, actual, expected)
	}
}

func BenchmarkDay04_Solve1(b *testing.B) {
	day, data := Day04{}, utils.ReadInputData(b, "year_2024/day_04.txt")
	for i := 0; i < b.N; i++ {
		day.Solve1(data)
	}
}

func BenchmarkDay04_Solve2(b *testing.B) {
	day, data := Day04{}, utils.ReadInputData(b, "year_2024/day_04.txt")
	for i := 0; i < b.N; i++ {
		day.Solve2(data)
	}
}
