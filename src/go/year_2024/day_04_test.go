package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day04 = Day04{}

func TestDay04_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 04, 1, "_example")
	if got := day04.Solve1(data); got != want {
		t.Fatalf(`day04.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay04_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2024, 04, 1, "")
	if got := day04.Solve1(data); got != want {
		t.Fatalf(`day04.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay04_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 04, 2, "_example")
	if got := day04.Solve2(data); got != want {
		t.Fatalf(`day04.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay04_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2024, 04, 2, "")
	if got := day04.Solve2(data); got != want {
		t.Fatalf(`day04.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay04_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2024, 04, 1, "")
	for i := 0; i < b.N; i++ {
		if day04.Solve1(data) != want {
			b.Fatal("day04.Solve1() is invalid")
		}
	}
}

func BenchmarkDay04_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2024, 04, 2, "")
	for i := 0; i < b.N; i++ {
		if day04.Solve2(data) != want {
			b.Fatal("day04.Solve2() is invalid")
		}
	}
}
