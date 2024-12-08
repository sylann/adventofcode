package year_2023

import (
	"testing"

	"github.com/sylann/adventofcode/utils"
)

var day06 = Day06{}

func TestDay06_Solve1_example(t *testing.T) {
	data, want := utils.GetData(t, 2023, 06, 1, "_example")
	if got := day06.Solve1(data); got != want {
		t.Fatalf(`day06.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay06_Solve1(t *testing.T) {
	data, want := utils.GetData(t, 2023, 06, 1, "")
	if got := day06.Solve1(data); got != want {
		t.Fatalf(`day06.Solve1() = %s; want %s`, got, want)
	}
}

func TestDay06_Solve2_example(t *testing.T) {
	data, want := utils.GetData(t, 2023, 06, 2, "_example")
	if got := day06.Solve2(data); got != want {
		t.Fatalf(`day06.Solve2() = %s; want %s`, got, want)
	}
}

func TestDay06_Solve2(t *testing.T) {
	data, want := utils.GetData(t, 2023, 06, 2, "")
	if got := day06.Solve2(data); got != want {
		t.Fatalf(`day06.Solve2() = %s; want %s`, got, want)
	}
}

func BenchmarkDay06_Solve1(b *testing.B) {
	data, want := utils.GetData(b, 2023, 06, 1, "")
	for i := 0; i < b.N; i++ {
		if day06.Solve1(data) != want {
			b.Fatal("day06.Solve1() is invalid")
		}
	}
}

func BenchmarkDay06_Solve2(b *testing.B) {
	data, want := utils.GetData(b, 2023, 06, 2, "")
	for i := 0; i < b.N; i++ {
		if day06.Solve2(data) != want {
			b.Fatal("day06.Solve2() is invalid")
		}
	}
}

