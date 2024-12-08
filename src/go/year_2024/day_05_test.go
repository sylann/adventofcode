package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day05 = Day05{}

func TestDay05_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 05, 1, "_example")
	if got := day05.Solve1(data); got != want {
		t.Fatalf(`day05.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay05_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2024, 05, 1, "")
	if got := day05.Solve1(data); got != want {
		t.Fatalf(`day05.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay05_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 05, 2, "_example")
	if got := day05.Solve2(data); got != want {
		t.Fatalf(`day05.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay05_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2024, 05, 2, "")
	if got := day05.Solve2(data); got != want {
		t.Fatalf(`day05.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay05_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2024, 05, 1, "")
	for i := 0; i < b.N; i++ {
		if day05.Solve1(data) != want {
			b.Fatal("day05.Solve1() is invalid")
		}
	}
}

func BenchmarkDay05_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2024, 05, 2, "")
	for i := 0; i < b.N; i++ {
		if day05.Solve2(data) != want {
			b.Fatal("day05.Solve2() is invalid")
		}
	}
}
