package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day03 = Day03{}

func TestDay03_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 03, 1, "_example")
	if got := day03.Solve1(data); got != want {
		t.Fatalf(`day03.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay03_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2024, 03, 1, "")
	if got := day03.Solve1(data); got != want {
		t.Fatalf(`day03.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay03_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 03, 2, "_example")
	if got := day03.Solve2(data); got != want {
		t.Fatalf(`day03.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay03_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2024, 03, 2, "")
	if got := day03.Solve2(data); got != want {
		t.Fatalf(`day03.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay03_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2024, 03, 1, "")
	for i := 0; i < b.N; i++ {
		if day03.Solve1(data) != want {
			b.Fatal("day03.Solve1() is invalid")
		}
	}
}

func BenchmarkDay03_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2024, 03, 2, "")
	for i := 0; i < b.N; i++ {
		if day03.Solve2(data) != want {
			b.Fatal("day03.Solve2() is invalid")
		}
	}
}
