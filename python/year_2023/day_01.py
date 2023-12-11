#!/usr/bin/env python3
import sys
import re
def eprint(*a, **kw): print(*a, **kw, file=sys.stderr)


def first_digit(line: str) -> int:
    return next((int(c) for c in line if c.isdigit()), 0)


def last_digit(line: str) -> int:
    return next((int(c) for c in reversed(line) if c.isdigit()), 0)


def solve_1(data: str) -> int:
    total = 0
    for line in data.strip().split("\n"):
        total += first_digit(line)*10 + last_digit(line)
    return total


def revstr(s: str) -> str:
    return "".join(reversed(s))


# I don't know how to efficiently seach backwards so I came with this idea of
# matching reversed number names in a reversed string
digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit1_re = re.compile(r"^.*?(\d|" + "|".join(digits) + ")")
digit2_re = re.compile(r"^.*?(\d|" + "|".join(map(revstr, digits)) + ")")


def to_digit_smart(s: str) -> int:
    return int(s) if s.isdigit() else digits.index(s)


def first_digit_smart(line: str) -> int:
    mo = digit1_re.match(line)
    return to_digit_smart(mo.group(1)) if mo else 0


def last_digit_smart(line: str) -> int:
    mo = digit2_re.match(revstr(line))
    return to_digit_smart(revstr(mo.group(1))) if mo else 0


def solve_2(data: str) -> int:
    total = 0
    for line in data.strip().split("\n"):
        total += first_digit_smart(line)*10 + last_digit_smart(line)
    return total


if __name__ == "__main__":
    # Part 1 can be solved with solve_2 but part 2 cannot be solved by solve_1
    data = sys.stdin.read()
    print("[PART 1]", solve_1(data), sep="\n")
    print("[PART 2]", solve_2(data), sep="\n")
