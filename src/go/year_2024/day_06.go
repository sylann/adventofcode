package year_2024

import (
	"fmt"
	"strconv"
	"strings"
	"time"
)

type Day06 struct{}

func init() {
	Solutions[06] = Day06{}
}

type direction int
type dcode int

const (
	Up direction = iota
	Right
	Down
	Left
)

var dirDebug = [4]dcode{1, 2, 4, 8} // bitarray for printing path on the grid
var moves = [4]vec2{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}

func (d direction) NextDir() direction {
	return (d + 1) % 4
}

type vec2 struct{ x, y int }

func (v vec2) InBound(w, h int) bool {
	return v.y >= 0 && v.y < h && v.x >= 0 && v.x < w
}

func (v vec2) Move(dir direction) vec2 {
	d := moves[dir]
	return vec2{v.x + d.x, v.y + d.y}
}

type trail struct {
	path      map[vec2]direction
	pathDebug map[vec2]dcode
	lastPos   vec2
	lastDir   direction
}

func NewTrail(pos vec2, dir direction) trail {
	path := make(map[vec2]direction)
	path2 := make(map[vec2]dcode)
	path[pos] = dir
	path2[pos] = dirDebug[dir]
	return trail{
		path:      path,
		pathDebug: path2,
		lastPos:   pos,
		lastDir:   dir,
	}
}

func (t *trail) Mark(pos vec2, dir direction) {
	t.path[pos] = dir
	t.MarkDir(pos, dir)
}

func (t *trail) MarkDir(pos vec2, dir direction) {
	t.pathDebug[pos] |= dirDebug[dir]
}

func findStart(g grid) vec2 {
	for y, row := range g.rows {
		for x, cell := range row {
			if cell == '^' {
				return vec2{x, y}
			}
		}
	}
	panic("unreachable: Could not find guard starting position")
}

func Show(g grid, t trail, start vec2, obstacles map[vec2]bool) {
	for y, row := range g.rows {
		for x, cell := range row {
			v := vec2{x, y}
			if v == start {
				fmt.Printf("\033[1;34mX\033[0m")
				continue
			}
			if obstacles[v] {
				fmt.Printf("\033[1;36mO\033[0m")
				continue
			}
			vs := t.pathDebug[v]
			switch vs {
			case 0:
				if cell == '#' {
					fmt.Printf("\033[1;37m%s\033[0m", "#")
				} else {
					fmt.Printf("\033[2;37m%s\033[0m", string(cell))
				}
			case dirDebug[Up]:                   fmt.Print("\033[1;31m^\033[0m")
			case dirDebug[Down]:                 fmt.Print("\033[1;31mv\033[0m")
			case dirDebug[Down]|dirDebug[Up]:    fmt.Print("\033[1;31m|\033[0m")
			case dirDebug[Left]:                 fmt.Print("\033[1;31m<\033[0m")
			case dirDebug[Right]:                fmt.Print("\033[1;31m>\033[0m")
			case dirDebug[Left]|dirDebug[Right]: fmt.Print("\033[1;31m-\033[0m")
			default:                             fmt.Print("\033[1;31m+\033[0m")
			}
		}
		fmt.Println()
	}
}

func (Day06) Solve1(data string) string {
	grid := NewGrid(data)
	start := findStart(grid)
	pos, dir := start, Up
	trail := NewTrail(pos, dir)
	for {
		npos := pos.Move(dir)
		if !npos.InBound(grid.w, grid.h) {
			break
		}
		if grid.rows[npos.y][npos.x] == '#' {
			dir = dir.NextDir()
			trail.MarkDir(pos, dir)
		} else {
			pos = npos
			trail.Mark(pos, dir)
		}
	}
	return strconv.Itoa(len(trail.path))
}

func TryObstacleAhead(g grid, st trail, obs, pos vec2, dir direction) bool {
	t := NewTrail(pos, dir)
	showLoopPath := false
	if showLoopPath {
		for k, v := range st.pathDebug {
			t.pathDebug[k] = v
		}
	}
	for {
		npos := pos.Move(dir)
		if !npos.InBound(g.w, g.h) {
			return false
		}
		d, seen := t.path[npos]
		if seen && d == dir {
			if showLoopPath {
				fmt.Println(strings.Repeat("=", 80))
				obstacles := make(map[vec2]bool)
				obstacles[obs] = true
				Show(g, t, pos, obstacles)
				time.Sleep(time.Second)
			}
			return true
		}
		if npos == obs || g.rows[npos.y][npos.x] == '#' {
			dir = dir.NextDir()
			t.MarkDir(pos, dir)
		} else {
			pos = npos
			t.Mark(pos, dir)
		}
	}
}

func (Day06) Solve2(data string) string {
	grid := NewGrid(data)
	start := findStart(grid)
	pos, dir := start, Up
	trail := NewTrail(pos, dir)
	obstacles := make(map[vec2]bool)
	for {
		npos := pos.Move(dir)
		if !npos.InBound(grid.w, grid.h) {
			break
		}
		if grid.rows[npos.y][npos.x] == '#' {
			dir = dir.NextDir()
			trail.MarkDir(pos, dir)
		} else {
			if npos != start && TryObstacleAhead(grid, trail, npos, start, Up) {
				obstacles[npos] = true
			}
			pos = npos
			trail.Mark(pos, dir)
		}
	}
	Show(grid, trail, start, obstacles)
	total := len(obstacles)
	return strconv.Itoa(total)
}
