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

// Resolve hand's HandType.
func (h Hand) Type(strengths string, useJoker bool) HandType {
	// Since there are always exactly 5 cards, the possible cases are limited and as follows:
	// Cards <=> asNum <=> Name          :  # Jokers => New Results
	// 5     <=> 50000 <=> FiveOfAKind   :  5|0      => 50000 | 50000
	// 41    <=> 41000 <=> FourOfAKind   :  4|1|0    => 50000 | 50000 | 41000
	// 32    <=> 32000 <=> FullHouse     :  3|2|0    => 50000 | 50000 | 32000
	// 311   <=> 31100 <=> ThreeOfAKind  :  3|1|0    => 41000 | 41000 | 31100
	// 221   <=> 22100 <=> TwoPairs      :  2|1|0    => 41000 | 32000 | 22100
	// 2111  <=> 21110 <=> OnePair       :  2|1|0    => 31100 | 31100 | 21110
	// 11111 <=> 11111 <=> HighCard      :  1|0      => 21110 | 11111
	nJok, cts := 0, make([]int, len(strengths))
	for _, c := range h {
		cts[c.Value(strengths)] += 1
	}
	if useJoker { // Memorize number of jokers before sorting
		nJok = cts[0] // at 0 because jokers are the weakest card
	}
	sort.Slice(cts, func(i1, i2 int) bool {
		return cts[i2] < cts[i1] // descending
	})
	asNum := 10000*cts[0] + 1000*cts[1] + 100*cts[2] + 10*cts[3] + 1*cts[4]
	switch {
	case asNum == 41000 && nJok != 0: return FiveOfAKind
	case asNum == 32000 && nJok != 0: return FiveOfAKind
	case asNum == 31100 && nJok != 0: return FourOfAKind
	case asNum == 22100 && nJok == 2: return FourOfAKind
	case asNum == 22100 && nJok == 1: return FullHouse
	case asNum == 21110 && nJok != 0: return ThreeOfAKind
	case asNum == 11111 && nJok == 1: return OnePair
	case asNum == 50000: return FiveOfAKind
	case asNum == 41000: return FourOfAKind
	case asNum == 32000: return FullHouse
	case asNum == 31100: return ThreeOfAKind
	case asNum == 22100: return TwoPair
	case asNum == 21110: return OnePair
	case asNum == 11111: return HighCard
	default: panic("Unreachable")
	}
}

// Represent a whole hand's sortable strength with a single, non-ambiguous integer.
func (h Hand) Strength(strengths string, useJoker bool) int {
	// There are 7 different hand type and 13 different cards.
	// So a base-13 number can represent everything without ambiguity.
	// Use pre-calculated base 13 powers to avoid using math.Pow and having to deal with casts.
	out := int(h.Type(strengths, useJoker)) * 371_293 // 13^5
	out += h[0].Value(strengths) * 28_561             // 13^4
	out += h[1].Value(strengths) * 2_197              // 13^3
	out += h[2].Value(strengths) * 169                // 13^2
	out += h[3].Value(strengths) * 13                 // 13^1
	out += h[4].Value(strengths) * 1                  // 13^0
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
