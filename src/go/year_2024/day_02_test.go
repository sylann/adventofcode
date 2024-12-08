package year_2024

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day02 = Day02{}

func TestDay02_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 02, 1, "_example")
	if got := day02.Solve1(data); got != want {
		t.Fatalf(`day02.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay02_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2024, 02, 1, "")
	if got := day02.Solve1(data); got != want {
		t.Fatalf(`day02.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay02_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2024, 02, 2, "_example")
	if got := day02.Solve2(data); got != want {
		t.Fatalf(`day02.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay02_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2024, 02, 2, "")
	if got := day02.Solve2(data); got != want {
		t.Fatalf(`day02.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay02_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2024, 02, 1, "")
	for i := 0; i < b.N; i++ {
		if day02.Solve1(data) != want {
			b.Fatal("day02.Solve1() is invalid")
		}
	}
}

func BenchmarkDay02_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2024, 02, 2, "")
	for i := 0; i < b.N; i++ {
		if day02.Solve2(data) != want {
			b.Fatal("day02.Solve2() is invalid")
		}
	}
}
