package year_2024

import (
	"slices"
	"strconv"
	"strings"
)

type Day05 struct{}

func init() {
	Solutions[05] = Day05{}
}

type safetyManual struct {
	rules   map[int][]int
	updates [][]int
}

func NewSafetyManual(data string) *safetyManual {
	parts := strings.Split(strings.TrimSpace(data), "\n\n")
	rulesRaw := strings.Split(parts[0], "\n")
	updatesRaw := strings.Split(parts[1], "\n")

	rules := make(map[int][]int)
	for _, line := range rulesRaw {
		// a line always has this format: NN|NN
		pageX, _ := strconv.Atoi(line[:2])
		pageY, _ := strconv.Atoi(line[3:])
		rules[pageY] = append(rules[pageY], pageX) // Y depends on X
	}

	updates := make([][]int, len(updatesRaw))
	for u, line := range updatesRaw {
		pagesRaw := strings.Split(line, ",")
		updates[u] = make([]int, len(pagesRaw))
		for p, page := range pagesRaw {
			updates[u][p], _ = strconv.Atoi(page)
		}
	}
	return &safetyManual{rules, updates}
}

// isValidUpdate returns whether an update respects all rules of the safety manual.
// Rules indicate which pages depend on which other pages. All pages must come in the
// proper order such that dependencies are satisfied.
func (sm *safetyManual) isValidUpdate(idx int) bool {
	forbidden := make(map[int]bool)
	for _, page := range sm.updates[idx] {
		isForbidden := forbidden[page]
		if isForbidden {
			return false
		}
		deps, hasDeps := sm.rules[page]
		if hasDeps {
			for _, dep := range deps {
				forbidden[dep] = true
			}
		}
	}
	return true
}

// fixUpdate sorts pages in the update of given idx such that rules are respected.
// Methodology:
// Careful data analysis indicates that each page always has 24 dependencies and
// that there are cyclic dependencies. Hence it is impossible to arrive at a general
// solution. However, a pattern emerges if we only consider pages of the current update.
// In this case, pages can be ordered by the number of current pages they depend on.
// So if a page has 0 dependencies in the current update, it should be last,
// and if it has `len(update)-1` dependencies, it should be first.
func (sm *safetyManual) fixUpdate(idx int) {
	depsByPage := make(map[int]int)
	update := sm.updates[idx]
	for _, page := range update {
		for _, dep := range sm.rules[page] {
			if slices.Contains(update, dep) {
				depsByPage[page]++
			}
		}
	}
	slices.SortFunc(sm.updates[idx], func(a, b int) int {
		return depsByPage[b] - depsByPage[a]
	})
}

func (sm *safetyManual) getMiddlePage(idx int) int {
	update := sm.updates[idx]
	middle := len(update) / 2
	middlePage := update[middle]
	return middlePage
}

func (Day05) Solve1(data string) string {
	sm := NewSafetyManual(data)
	total := 0
	for i := range sm.updates {
		if sm.isValidUpdate(i) {
			total += sm.getMiddlePage(i)
		}
	}
	return strconv.Itoa(total)
}

func (Day05) Solve2(data string) string {
	sm := NewSafetyManual(data)
	total := 0
	for i := range sm.updates {
		if !sm.isValidUpdate(i) {
			sm.fixUpdate(i)
			total += sm.getMiddlePage(i)
		}
	}
	return strconv.Itoa(total)
}
