#!/usr/bin/env python3
import functools
import sys
def eprint(*a, **kw): print(*a, **kw, file=sys.stderr)


def solve_1(data: str):
    total = 0
    for line in data.strip().split("\n"):
        _, nums = line.split(": ")
        winning, owned = (set(x.split()) for x in nums.split(" | "))

        n_matching = len(winning & owned)
        if n_matching:
            total += 2 ** (n_matching - 1)

    return total


def solve_2(data: str):
    copies_by_card = {}
    for line in data.strip().split("\n"):
        card, nums = line.split(": ")
        id_ = int(card.removeprefix("Card "))
        winning, owned = (set(x.split()) for x in nums.split(" | "))

        n_matching = len(winning & owned)
        copies_by_card[id_] = tuple(range(id_ + 1, id_ + 1 + n_matching))

    @functools.cache
    def count(cards: tuple[int]):
        return sum(1 + count(copies_by_card.get(c, ())) for c in cards)

    return count(tuple(copies_by_card))


if __name__ == "__main__":
    data = sys.stdin.read()
    print("[PART 1]", solve_1(data), sep="\n")
    print("[PART 2]", solve_2(data), sep="\n")
