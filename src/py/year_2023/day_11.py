import itertools as it
from py.utils.debug import eprint


def sum_distances(data: str, scale: int) -> int:
    grid = data.strip().split("\n")

    width = len(grid[0])
    height = len(grid)
    empty_x = [x for x in range(width) if all(grid[y][x] == "." for y in range(height))]
    empty_y = [y for y in range(height) if all(grid[y][x] == "." for x in range(width))]
    # print("empty_x", empty_x)
    # print("empty_y", empty_y)

    def adjust_coords(x: int, y: int, scale: int):
        new_x = x + (scale-1) * sum(1 for ex in empty_x if ex < x)
        new_y = y + (scale-1) * sum(1 for ey in empty_y if ey < y)
        # print(f"ADJUST COORDS: {x},{y} -> {new_x},{new_y}")
        return new_x, new_y

    galaxies: list[tuple[int, int]] = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ".":
                galaxies.append(adjust_coords(x, y, scale))

    total = 0
    for ((x1, y1), (x2, y2)) in it.combinations(galaxies, 2):
        dist = abs(y2 - y1) + abs(x2 - x1)
        # print("DIST +=", dist)
        total += dist

    return total


def solve_1(data: str):
    return str(sum_distances(data, 2))


def solve_2(data: str):
    return str(sum_distances(data, 1000000))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
