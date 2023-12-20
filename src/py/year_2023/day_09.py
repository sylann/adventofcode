from py.utils.debug import eprint


def generate_deltas(line: str):
    values = [int(x) for x in line.split()]
    sequences: list[list[int]] = [values]
    while True:
        next_lvl = [n - values[i-1] for i, n in enumerate(values[1:], start=1)]
        if not any(next_lvl):
            break
        values = next_lvl
        sequences.append(values)

    while sequences:
        yield sequences.pop()


def extrapolate_left(line: str):
    newval = 0
    for lvl, values in enumerate(generate_deltas(line)):
        newval = values[0] - newval
        if __debug__: eprint(f"Left L{lvl}: ", newval, values)
    return newval


def extrapolate_right(line: str):
    newval = 0
    for lvl, values in enumerate(generate_deltas(line)):
        newval = values[-1] + newval
        if __debug__: eprint(f"Right L{lvl}: ", values, newval)
    return newval


def solve_1(data: str):
    return sum(extrapolate_right(line) for line in data.strip().split("\n"))


def solve_2(data: str):
    return sum(extrapolate_left(line) for line in data.strip().split("\n"))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
