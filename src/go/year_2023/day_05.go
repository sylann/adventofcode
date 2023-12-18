package year_2023

import (
	"fmt"
	"strconv"
	"strings"
)

type MapRange struct {
	Dst  int
	Src  int
	Size int
}

type CategoryMap struct {
	DstId  string
	Ranges []MapRange
}

type Almanac struct {
	Seeds []int
	Maps  map[string]*CategoryMap
}

// Parse seeds and maps from the given data.
func NewAlmanac(data string) *Almanac {
	data = strings.TrimSpace(data)
	lines := strings.Split(data, "\n")

	a := Almanac{}
	a.parseSeeds(&lines)
	a.parseMaps(&lines)
	return &a
}

func (a *Almanac) parseSeeds(dataLines *[]string) {
	rawSeeds := strings.Split((*dataLines)[0], " ")[1:]
	a.Seeds = make([]int, len(rawSeeds))
	for i, s := range rawSeeds {
		a.Seeds[i], _ = strconv.Atoi(s)
	}
	// fmt.Fprintf(os.Stderr, "Seeds = %#v\n", a.Seeds)
}

func (a *Almanac) parseMaps(dataLines *[]string) {
	a.Maps = make(map[string]*CategoryMap)

	var cur *CategoryMap
	for _, line := range (*dataLines)[2:] {
		if cur == nil {
			var srcId string
			cur = new(CategoryMap)
			cur.Ranges = make([]MapRange, 0)

			line = strings.Replace(line, "-", " ", 2)
			fmt.Sscanf(line, "%s to %s map:", &srcId, &cur.DstId)

			a.Maps[srcId] = cur
		} else if line != "" {
			var r = MapRange{}
			fmt.Sscanf(line, "%d %d %d", &r.Dst, &r.Src, &r.Size)

			cur.Ranges = append(cur.Ranges, r)
		} else {
			cur = nil
		}
	}
}

// Convert a value "num" from category "srcId" to category "targetId".
func (a *Almanac) Convert(srcId, targetId string, num, nAfter int) (int, int) {
	// fmt.Fprintf(os.Stderr, "%d -> ", num)
	if srcId == targetId {
		// fmt.Fprintf(os.Stderr, "%d | Skippable: %d\n", num, nAfter)
		return num, nAfter
	}

	var nBefore int
	for _, rng := range a.Maps[srcId].Ranges {
		if rng.Src <= num && num < rng.Src+rng.Size {
			nBefore = num - rng.Src
			nAfter = min(nAfter, rng.Size-nBefore)
			num = rng.Dst + nBefore
			break
		}
	}

	return a.Convert(a.Maps[srcId].DstId, targetId, num, nAfter)
}

func (a *Almanac) String() string {
	var sb = strings.Builder{}
	for src, m := range a.Maps {
		fmt.Fprintf(&sb, "CategoryMap: %s -> %s\n  Ranges:\n", src, m.DstId)
		for _, r := range m.Ranges {
			fmt.Fprintf(&sb, "    %d -> %d [%d]\n", r.Src, r.Dst, r.Size)
		}
	}
	return sb.String()
}

type Day05 struct{}

func init() {
	Solutions[05] = Day05{}
}

func (Day05) Solve1(data string) string {
	alma := NewAlmanac(data)
	// fmt.Fprintln(os.Stderr, alma.String())

	var loc, seed int
	var minLoc = 1_000_000_000_000 // Largely enough
	for _, seed = range alma.Seeds {
		loc, _ = alma.Convert("seed", "location", seed, 1)
		minLoc = min(minLoc, loc)
	}
	return fmt.Sprint(minLoc)
}

func (Day05) Solve2(data string) string {
	alma := NewAlmanac(data)
	// fmt.Fprintln(os.Stderr, alma.String())

	var loc, skip, seed, nSeeds, i int
	var minLoc = 1_000_000_000_000 // Largely enough
	for i = 0; i < len(alma.Seeds); i += 2 {
		seed = alma.Seeds[i]
		nSeeds = alma.Seeds[i+1]
		for nSeeds > 0 {
			loc, skip = alma.Convert("seed", "location", seed, nSeeds)
			minLoc = min(minLoc, loc)
			seed += skip
			nSeeds -= skip
		}
	}
	return fmt.Sprint(minLoc)
}
