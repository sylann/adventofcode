#!/usr/bin/env python3
import sys
import typing as t

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----

priorities = {
    **{chr(ord('a') + x): x + 1 for x in range(0, 26)},
    **{chr(ord('A') + x): x + 27 for x in range(0, 26)},
}


def iter_common_in_rs_halves(data: str) -> t.Generator[set[str], None, None]:
    for rucksack in data.strip().split("\n"):
        half_size = len(rucksack) // 2
        c1, c2 = rucksack[:half_size], rucksack[half_size:]

        yield set(c1) & set(c2)

def iter_common_in_3_rs(data: str) -> t.Generator[set[str], None, None]:
    rucksacks = data.strip().split("\n")

    for i in range(0, len(rucksacks), 3):
        yield set(rucksacks[i]) & set(rucksacks[i + 1]) & set(rucksacks[i + 2])


def count_priority(it: t.Iterator[set[str]]) -> int:
    commons = []

    for common in it:
        __(f"common = {common}")
        commons += common

    return sum(priorities[c] for c in commons)


print("1:", count_priority(iter_common_in_rs_halves(data)))
print("2:", count_priority(iter_common_in_3_rs(data)))
