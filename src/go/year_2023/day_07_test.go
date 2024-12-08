package year_2023

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day07 = Day07{}

func TestDay07_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2023, 07, 1, "_example")
	if got := day07.Solve1(data); got != want {
		t.Fatalf(`day07.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay07_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2023, 07, 1, "")
	if got := day07.Solve1(data); got != want {
		t.Fatalf(`day07.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay07_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2023, 07, 2, "_example")
	if got := day07.Solve2(data); got != want {
		t.Fatalf(`day07.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay07_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2023, 07, 2, "")
	if got := day07.Solve2(data); got != want {
		t.Fatalf(`day07.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay07_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2023, 07, 1, "")
	for i := 0; i < b.N; i++ {
		if day07.Solve1(data) != want {
			b.Fatal("day07.Solve1() is invalid")
		}
	}
}

func BenchmarkDay07_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2023, 07, 2, "")
	for i := 0; i < b.N; i++ {
		if day07.Solve2(data) != want {
			b.Fatal("day07.Solve2() is invalid")
		}
	}
}

