def get_elves(data: str):
    elves = [sum(map(int, elf.split("\n"))) for elf in data.strip().split("\n\n")]
    elves.sort(reverse=True)
    return elves


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    elves = get_elves(data)
    print("\n[PART 1]", elves[0], sep="\n")
    print("\n[PART 2]", sum(elves[:3]), sep="\n")
