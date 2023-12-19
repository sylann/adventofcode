package year_2023

import (
	"cmp"
	"fmt"
	"slices"
	"sort"
	"strconv"
	"strings"
)

// https://cs.opensource.google/go/go/+/master:src/cmp/cmp.go;l=61
// Or returns the first of its arguments that is not equal to the zero value.
// If no argument is non-zero, it returns the zero value.
func Or[T comparable](vals ...T) T {
	var zero T
	for _, val := range vals {
		if val != zero {
			return val
		}
	}
	return zero
}

type HandType int

const (
	HighCard HandType = iota + 1
	OnePair
	TwoPair
	ThreeOfAKind
	FullHouse
	FourOfAKind
	FiveOfAKind
)

// Card is one of: A K Q J T 9 8 7 6 5 4 3 2
type Card byte

func (c Card) Value(strengths string) int {
	return strings.IndexByte(strengths, byte(c))
}

type Hand []Card // ordered slice of 5 Cards

func (h Hand) Type(strengths string, useJoker bool) HandType {
	countByValue := make([]int, len(strengths))
	for _, c := range h {
		countByValue[c.Value(strengths)] += 1
	}

	orderedCounts := make([]int, len(strengths))
	copy(orderedCounts, countByValue)
	sort.Slice(orderedCounts, func(i1, i2 int) bool {
		return orderedCounts[i2] < orderedCounts[i1] // descending
	})

	jokerCount := 0
	if useJoker {
		// By definition, the joker is the weakest card (hence, take the value at 0)
		jokerCount = countByValue[0]
	}

	// Now, there is only a 7 possible results without jokers, and some variations with jokers:
	// Cards      -> Type  "name"              With n Jokers  ->  Types
	// 5          -> 5     "Five of a Kind"    5|0            ->  5
	// 4+1        -> 4     "Four of a Kind"    4|1|0          ->  5|5|3+2
	// 3+2        -> 3+2   "Full house"        3|2|0          ->  5|5|3+2
	// 3+1+1      -> 3     "Three of a Kind"   3|1|0          ->  4|4|3
	// 2+2+1      -> 2+2   "Two Pairs"         2|1|0          ->  4|3+2|2+2
	// 2+1+1+1    -> 2     "One Pair"          2|1|0          ->  3|3|2
	// 1+1+1+1+1  -> 1     "High Card"         1|0            ->  2|1

	if orderedCounts[0] == 5 { // 5
		return FiveOfAKind
	}
	if orderedCounts[0] == 4 { // 4+1
		if jokerCount != 0 {
			return FiveOfAKind
		}
		return FourOfAKind
	}
	if orderedCounts[0] == 3 { // 3+2 or 3+1+1
		if orderedCounts[1] == 2 {
			if jokerCount != 0 {
				return FiveOfAKind
			}
			return FullHouse
		}
		if jokerCount != 0 {
			return FourOfAKind
		}
		return ThreeOfAKind
	}
	if orderedCounts[0] == 2 { // 2+2+1 or 2+1+1+1
		if orderedCounts[1] == 2 {
			if jokerCount == 2 {
				return FourOfAKind
			}
			if jokerCount == 1 {
				return FullHouse
			}
			return TwoPair
		}
		if jokerCount != 0 {
			return ThreeOfAKind
		}
		return OnePair
	}
	if jokerCount != 0 { // 1+1+1+1+1
		return OnePair
	}
	return HighCard
}

// Represent a whole hand's sortable strength with a single, non-ambiguous integer.
func (h Hand) Strength(strengths string, useJoker bool) int {
	ht := int(h.Type(strengths, useJoker))
	v0 := h[0].Value(strengths)
	v1 := h[1].Value(strengths)
	v2 := h[2].Value(strengths)
	v3 := h[3].Value(strengths)
	v4 := h[4].Value(strengths)
	// There are 7 different hand type and 13 different cards.
	// So a base-13 number can represent everything without ambiguity.
	out := ht * 4826809 // 13^6  (pre evaluated to avoid using math.pow)
	out += v0 * 371293  // 13^5
	out += v1 * 28561   // 13^4
	out += v2 * 2197    // 13^3
	out += v3 * 169     // 13^2
	out += v4 * 13      // 13^1
	// fmt.Fprintf(os.Stderr, "%9d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t", out, ht, v0, v1, v2, v3, v4, h)
	return out
}

type Game struct {
	strength int
	bid      int
}

func CountWinnings(data, strengths string, useJoker bool) int {
	data = strings.TrimSpace(data)
	lines := strings.Split(data, "\n")

	games := make([]Game, len(lines))
	for i, line := range lines {
		hand := Hand(line[:5])
		bid, _ := strconv.Atoi(line[6:])
		strength := hand.Strength(strengths, useJoker)
		// fmt.Fprintf(os.Stderr, "%d\n", bid)
		games[i] = Game{strength, bid}
	}

	slices.SortFunc(games, func(a, b Game) int {
		return cmp.Compare(a.strength, b.strength)
	})

	total := 0
	for i, game := range games {
		total += (i + 1) * game.bid
	}
	return total
}

type Day07 struct{}

func init() {
	Solutions[07] = Day07{}
}

func (Day07) Solve1(data string) string {
	winnings := CountWinnings(data, "23456789TJQKA", false)
	return fmt.Sprint(winnings)
}

func (Day07) Solve2(data string) string {
	winnings := CountWinnings(data, "J23456789TQKA", true)
	return fmt.Sprint(winnings)
}
