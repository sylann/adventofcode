package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day01 = Day01{}

func TestDay01_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 01, 1, "_example")
	if got := day01.Solve1(data); got != want {
		t.Fatalf(`day01.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay01_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2024, 01, 1, "")
	if got := day01.Solve1(data); got != want {
		t.Fatalf(`day01.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay01_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 01, 2, "_example")
	if got := day01.Solve2(data); got != want {
		t.Fatalf(`day01.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay01_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2024, 01, 2, "")
	if got := day01.Solve2(data); got != want {
		t.Fatalf(`day01.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay01_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2024, 01, 1, "")
	for i := 0; i < b.N; i++ {
		if day01.Solve1(data) != want {
			b.Fatal("day01.Solve1() is invalid")
		}
	}
}

func BenchmarkDay01_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2024, 01, 2, "")
	for i := 0; i < b.N; i++ {
		if day01.Solve2(data) != want {
			b.Fatal("day01.Solve2() is invalid")
		}
	}
}
