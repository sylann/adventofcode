package year_2024

import (
	"fmt"
	"strconv"
)

type Day03 struct{}

func init() {
	Solutions[03] = Day03{}
}

// NOTE: Deliberately not using RegExp for the sport.
// It would be way simpler obviously.

// matchInteger expects to match a valid integer at the start of the given data.
// If it does, it returns true, remaining data, and the matched integer.
// Otherwise, it returns false, the given data, and 0.
func matchInteger(data string) (ok bool, remaining string, matched int) {
	i := 0
	size := len(data)
	for ; i < size && data[i] >= '0' && data[i] <= '9'; i++ {
	}
	if i == 0 {
		return false, data, 0 // matched no digit at all
	}
	matched, _ = strconv.Atoi(data[:i])
	return true, data[i:], matched
}

// literalMatcher returns a function that matches the given literal.
// The returned function expects to match the literal at the start of the given data.
// If it does, it returns true and remaining data.
// Otherwise, it returns false and the given data.
func literalMatcher(lit string) func(string) (bool, string) {
	size := len(lit)
	return func(data string) (ok bool, remaining string) {
		if size <= len(data) && data[:size] == lit {
			return true, data[size:]
		}
		return false, data
	}
}

var matchStart = literalMatcher("mul(")
var matchSep = literalMatcher(",")
var matchEnd = literalMatcher(")")

// matchMulExpression expects to match a valid mul(int,int) expression
// at the start of the given data.
// If it does, it returns true, remaining data and the result of `int * int`.
// Otherwise, it returns false, the given data and 0.
func matchMulExpression(data string) (ok bool, rem string, result int) {
	var num1, num2 int
	rem = data
	if ok, rem = matchStart(rem); !ok {
		return false, data, 0
	}
	if ok, rem, num1 = matchInteger(rem); !ok {
		return false, data, 0
	}
	if ok, rem = matchSep(rem); !ok {
		return false, data, 0
	}
	if ok, rem, num2 = matchInteger(rem); !ok {
		return false, data, 0
	}
	if ok, rem = matchEnd(rem); !ok {
		return false, data, 0
	}
	return true, rem, num1 * num2
}

// Solve1 computes the sum of all valid `mul(int,int)` expressions.
func (Day03) Solve1(data string) string {
	total := 0
	for data != "" {
		ok, rem, result := matchMulExpression(data)
		if ok {
			total += result
			data = rem
		} else {
			data = data[1:]
		}
	}
	return fmt.Sprintf("%d", total)
}

var matchDo = literalMatcher("do()")
var matchDont = literalMatcher("don't()")

// Solve2 computes the sum of all valid `mul(int,int)` expressions
// that are not previouly disabled by a `don't()` expression.
// The `do()` expression cancels this effect.
func (Day03) Solve2(data string) string {
	total := 0
	enabled := true
	for data != "" {
		if enabled {
			if ok, rem, result := matchMulExpression(data); ok {
				total += result
				data = rem
				continue
			}
			if ok, rem := matchDont(data); ok {
				enabled = false
				data = rem
				continue
			}
		} else {
			if ok, rem := matchDo(data); ok {
				enabled = true
				data = rem
				continue
			}
		}
		data = data[1:] // go to next char
	}
	return fmt.Sprintf("%d", total)
}
