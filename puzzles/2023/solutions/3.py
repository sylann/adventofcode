#!/usr/bin/env python3
import collections
import sys

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----

class Grid:
    def __init__(self, data: str) -> None:
        self._grid = [list(line) for line in data.strip().split("\n")]
        self.MAX_X = len(self._grid[0]) - 1
        self.MAX_Y = len(self._grid) - 1

    def peek(self, x: int, y: int) -> str:
        return self._grid[y][x]

    def iter_nums(self):
        for y, row in enumerate(self._grid):
            num = None
            for x, cell in enumerate(row):
                if cell.isdigit():
                    if num is None:
                        num = [x, y, cell]
                    else:
                        num[2] += cell
                elif num is not None:
                    yield num
                    num = None
            if num is not None: # row ended with a num
                yield num

    def iter_cells_around_num(self, x: int, y: int, size: int):
        x_rng = range(max(0, x-1), min(x+size, self.MAX_X) + 1)
        if x > 0:                   yield x-1, y                            # LEFT
        if x+size <= self.MAX_X:    yield x+size, y                         # RIGHT
        if y > 0:                   yield from ((xi, y-1) for xi in x_rng)  # ROW ABOVE
        if y < self.MAX_Y:          yield from ((xi, y+1) for xi in x_rng)  # ROW BELOW
        

def solve_1(data: str) -> int:
    grid = Grid(data)
    total = 0

    for xn, yn, num in grid.iter_nums():
        for xa, ya in grid.iter_cells_around_num(xn, yn, len(num)):
            c = grid.peek(xa, ya)
            if c != "." and not c.isdigit():
                total += int(num)
                break

    return total


def solve_2(data: str) -> int:
    grid = Grid(data)
    gears = collections.defaultdict(list)

    for xn, yn, num in grid.iter_nums():
        for xa, ya in grid.iter_cells_around_num(xn, yn, len(num)):
            if grid.peek(xa, ya) == "*":
                gears[(xa, ya)].append(int(num))

    total = 0
    for nums in gears.values():
        if len(nums) == 2:
            total += nums[0] * nums[1]
    return total


print("1:", solve_1(data))
print("2:", solve_2(data))
