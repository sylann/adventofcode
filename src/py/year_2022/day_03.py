import typing as t

from py.utils.debug import eprint


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
        if __debug__: eprint(f"common = {common}")
        commons += common

    return sum(priorities[c] for c in commons)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    sol_1 = count_priority(iter_common_in_rs_halves(data))
    sol_2 = count_priority(iter_common_in_3_rs(data))
    print("[PART 1]", sol_1, sep="\n")
    print("[PART 2]", sol_2, sep="\n")
