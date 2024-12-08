package year_2024

import (
	"strconv"
	"strings"
)

type Day04 struct{}

func init() {
	Solutions[04] = Day04{}
}

type search struct{ x0, y0, x1, y1, x2, y2, x3, y3 int }

var horizontal = search{0, 0, 1, 0, 2, 0, 3, 0}
var vertical = search{0, 0, 0, 1, 0, 2, 0, 3}
var diagonal1 = search{0, 0, 1, 1, 2, 2, 3, 3}
var diagonal2 = search{0, 3, 1, 2, 2, 1, 3, 0}

type grid []string

func NewGrid(data string) grid {
	return strings.Split(strings.TrimSpace(data), "\n")
}

func (g grid) Search1(s search, x, y int) int {
	c0 := g[y+s.y0][x+s.x0]
	c1 := g[y+s.y1][x+s.x1]
	c2 := g[y+s.y2][x+s.x2]
	c3 := g[y+s.y3][x+s.x3]
	forward := c0 == 'X' && c1 == 'M' && c2 == 'A' && c3 == 'S'
	backward := c3 == 'X' && c2 == 'M' && c1 == 'A' && c0 == 'S'
	if forward || backward {
		return 1
	}
	return 0
}

func (Day04) Solve1(data string) string {
	grid := NewGrid(data)
	w, h := len(grid[0]), len(grid)
	out := 0
	for y := 0; y < h; y++ {
		for x := 0; x < w-3; x++ {
			out += grid.Search1(horizontal, x, y)
		}
	}
	for y := 0; y < h-3; y++ {
		for x := 0; x < w; x++ {
			out += grid.Search1(vertical, x, y)
		}
	}
	for y := 0; y < h-3; y++ {
		for x := 0; x < w-3; x++ {
			out += grid.Search1(diagonal1, x, y) + grid.Search1(diagonal2, x, y)
		}
	}
	return strconv.Itoa(out)
}

func (g grid) Search2(x, y int) int {
	if g[y][x] != 'A' {
		return 0
	}
	a := g[y-1][x-1] //   A +-----+ B
	b := g[y-1][x+1] //     |     |
	c := g[y+1][x+1] //     |     |
	d := g[y+1][x-1] //   D +-----+ C
	ac := a == 'M' && c == 'S'
	ca := c == 'M' && a == 'S'
	bd := b == 'M' && d == 'S'
	db := d == 'M' && b == 'S'
	if ac && db || ac && bd || ca && db || ca && bd {
		return 1
	}
	return 0
}

func (Day04) Solve2(data string) string {
	grid := NewGrid(data)
	w, h := len(grid[0]), len(grid)
	out := 0
	for y := 1; y < h-1; y++ {
		for x := 1; x < w-1; x++ {
			out += grid.Search2(x, y)
		}
	}
	return strconv.Itoa(out)
}
