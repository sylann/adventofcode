package year_2024

import (
	"strconv"
	"strings"
)

type Day04 struct{}

func init() {
	Solutions[04] = Day04{}
}

type search struct{ ax, ay, bx, by, cx, cy, dx, dy, w, h int }

var horizontal = search{0, 0, 1, 0, 2, 0, 3, 0, 4, 1}
var vertical = search{0, 0, 0, 1, 0, 2, 0, 3, 1, 4}
var diagonal1 = search{0, 0, 1, 1, 2, 2, 3, 3, 4, 4}
var diagonal2 = search{0, 3, 1, 2, 2, 1, 3, 0, 4, 4}

type grid struct {
	// INFO: having width and height together with rows in the struct
	// noticeably improves performance. Better memory caching?
	rows []string
	w, h int
}

func NewGrid(data string) grid {
	rows := strings.Split(strings.TrimSpace(data), "\n")
	w, h := len(rows[0]), len(rows)
	return grid{rows, w, h}
}

// INFO: Just comparing arrays instead of multiple individual bytes
// makes the code run much much faster.
var XMAS = [4]byte{'X', 'M', 'A', 'S'}
var SAMX = [4]byte{'S', 'A', 'M', 'X'}

func (g grid) Search(s search) int {
	w := g.w - s.w + 1
	h := g.h - s.h + 1
	total := 0
	for y := 0; y < h; y++ {
		// INFO: avoiding y access on each x loop is a critical performance improvement
		ay, by, cy, dy := g.rows[y+s.ay], g.rows[y+s.by], g.rows[y+s.cy], g.rows[y+s.dy]
		for x := 0; x < w; x++ {
			word := [4]byte{ay[x+s.ax], by[x+s.bx], cy[x+s.cx], dy[x+s.dx]}
			if word == XMAS || word == SAMX {
				total++
			}
		}
	}
	return total
}

func (Day04) Solve1(data string) string {
	g := NewGrid(data)
	total := g.Search(horizontal) + g.Search(vertical) + g.Search(diagonal1) + g.Search(diagonal2)
	return strconv.Itoa(total)
}

//   A +-----+ B
//     |     |
//     |     |
//   D +-----+ C    A    B    C    D
var MMSS = [4]byte{'M', 'M', 'S', 'S'}
var MSSM = [4]byte{'M', 'S', 'S', 'M'}
var SSMM = [4]byte{'S', 'S', 'M', 'M'}
var SMMS = [4]byte{'S', 'M', 'M', 'S'}

func (Day04) Solve2(data string) string {
	g := NewGrid(data)
	total := 0
	for y, maxY := 1, g.h-1; y < maxY; y++ {
		row0, row1, row2 := g.rows[y-1], g.rows[y], g.rows[y+1]
		for x, maxX := 1, g.w-1; x < maxX; x++ {
			if row1[x] == 'A' {
				word := [4]byte{row0[x-1], row0[x+1], row2[x+1], row2[x-1]}
				if word == MMSS || word == MSSM || word == SSMM || word == SMMS {
					total += 1
				}
			}
		}
	}
	return strconv.Itoa(total)
}
