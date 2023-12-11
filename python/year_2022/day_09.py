#!/usr/bin/env python3
import itertools
import sys
import typing as t

__ = lambda *a, **kw: print(*a, **kw, file=sys.stderr)

# ----- START OF SOLUTION -----


Direction = t.Literal["U", "D", "L", "R"]
Coord = tuple[int, int]


class Vec2(t.NamedTuple):
    x: int
    y: int

    def __add__(self, other: Coord) -> t.Self:
        x, y = other
        return self.__class__(self.x + x, self.y + y)

    def __sub__(self, other: Coord) -> t.Self:
        x, y = other
        return self.__class__(self.x - x, self.y - y)

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


class Knot(Vec2):
    def follow(self, other: Vec2) -> t.Self:
        x, y = self
        dx, dy = other - self

        assert abs(dx) < 3 and abs(dy) < 3

        if dx == 2:
            x += 1
            y += dy if dy in (-1, 1) else 0
        elif dx == -2:
            x -= 1
            y += dy if dy in (-1, 1) else 0

        if dy == 2:
            y += 1
            x += dx if dx in (-1, 1) else 0
        elif dy == -2:
            y -= 1
            x += dx if dx in (-1, 1) else 0

        assert x >= 0 and y >= 0

        return self.__class__(x, y)


class Simulation:
    moves: list[Vec2]
    width: int
    height: int
    initial_pos: Vec2

    _delta_by_direction: dict[Direction, Vec2] = {
        "U": Vec2(0, -1),
        "D": Vec2(0, 1),
        "L": Vec2(-1, 0),
        "R": Vec2(1, 0),
    }

    def __init__(self, move_scheme: str) -> None:
        self.moves = self.parse_moves(move_scheme)
        (min_x, min_y), (max_x, max_y) = self.get_boundaries(self.moves)
        self.width = max_x - min_x + 1
        self.height = max_y - min_y + 1
        self.initial_pos = Vec2(-min_x, -min_y)
        __(
            f"Grid({self.width}x{self.height}): x=[{min_x},{max_x}] y=[{min_y},{max_y}]"
            + f" start={self.initial_pos}"
        )

    @classmethod
    def parse_moves(cls, move_scheme: str) -> list[Vec2]:
        out = []
        for line in move_scheme.strip("\n").split("\n"):
            dir, n = line.split()
            assert dir in cls._delta_by_direction, f"Unexpected direction: {dir}"
            out += int(n) * [cls._delta_by_direction[dir]]
        return out

    @classmethod
    def get_boundaries(cls, moves: list[Vec2]) -> tuple[Coord, Coord]:
        xs, ys = zip(*itertools.accumulate(moves))
        return (min(xs), min(ys)), (max(xs), max(ys))

    def repr_state(self, rope: list[Vec2]) -> str:
        grid = [
            [" " if x % 5 and y % 5 else "." for x in range(self.width)]
            for y in range(self.height)
        ]

        names = ("H", *map(str, range(1, len(rope) - 1)), "T")
        # rope contains knots from head to tail. Reverse the list so that when
        # a given position contains several knots we show the one closer to head.
        for (x, y), name in zip(reversed(rope), reversed(names)):
            grid[y][x] = name

        # Add ticks
        cell = lambda v: f"{v:>3}"
        tick = lambda i: cell(" ") if i % 5 else cell(i)
        grid = [
            cell(" ") + "".join(map(tick, range(self.width))),
            *(tick(i) + "".join(map(cell, row)) for i, row in enumerate(grid))
        ]
        # Add metadata on the left side of the grid
        return "\n".join(
            f"{name:<3}{str(k):<8}{row}"
            for row, k, name in itertools.zip_longest(grid, rope, names, fillvalue="")
        )

    def count_visited(self, rope_size: int) -> int:
        if rope_size < 2:
            raise ValueError("A rope must have at least 2 knots")

        H = T = Knot(*self.initial_pos)  # Knot is immutable, no need to copy
        mid_knots = (rope_size - 2) * [T]

        visited_by_tail = set()
        visited_by_tail.add(T)
        __(f"== Initial State ==\n\n{self.repr_state([H, *mid_knots, T])}\n")

        for mi, move in enumerate(self.moves):
            H = H + move

            leading = H
            for i, following in enumerate(mid_knots):
                leading = mid_knots[i] = following.follow(leading)

            T = T.follow(leading)
            visited_by_tail.add(T)
            __(f"== [{mi}] {move} ==\n\n{self.repr_state([H, *mid_knots, T])}\n")

        return len(visited_by_tail)


if __name__ == "__main__":
    data = sys.stdin.read()
    sim = Simulation(data)
    print("[PART 1]", sim.count_visited(rope_size=2), sep="\n")
    print("[PART 2]", sim.count_visited(rope_size=10), sep="\n")
