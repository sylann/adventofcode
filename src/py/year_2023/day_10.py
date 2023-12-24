from py.utils.debug import eprint

opened_by_dir = {
    "up": "F7|",
    "right": "7J-",
    "down": "LJ|",
    "left": "FL-",
}
directions = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}
opposite = {
    "up": "down",
    "right": "left",
    "down": "up",
    "left": "right",
}
pretty = dict(zip("F7JL|-", "┏┓┛┗┃━"))


class Grid:
    def __init__(self, data: str) -> None:
        self._grid = data.strip().split("\n")

    def find_start(self):
        for y, row in enumerate(self._grid):
            for x, cell in enumerate(row):
                if cell == "S":
                    return x, y
        raise RuntimeError("Unreachable")

    def look_around(self, cx: int, cy: int, origin: str):
        for dir in set(directions) - {origin}:
            dx, dy = directions[dir]
            x, y = cx+dx, cy+dy
            yield x, y, dir

    def walk_loop(self, x: int, y: int):
        origin = "up" # initial dir is irrelevant and arbitrary
        # NOTE: All pipes have 2 openings. As long as the current position is a pipe,
        # a next cell must exist. For this reason, variables can be overwritten safely.
        while True:
            if __debug__: eprint(f"FROM {origin:<5}  {x},{y}")
            cell = self._grid[y][x]
            for x, y, dir in self.look_around(x, y, origin):
                origin = opposite[dir]
                if cell == "S" or cell in opened_by_dir[origin]:
                    next_cell = self._grid[y][x]
                    if __debug__: eprint(f"     LOOK {dir:<5}  {x},{y}  {next_cell}")

                    if next_cell == "S":
                        yield x, y, next_cell
                        return

                    if next_cell in opened_by_dir[dir]:
                        yield x, y, next_cell
                        break
            else:
                raise RuntimeError(f"Unreachable: {x},{y} {origin}")

    def scan_topology(self):
        sx, sy = self.find_start()
        loop_cells = set((x, y) for x, y, _ in self.walk_loop(sx, sy))
        topo_changing_pair = {"F": "J", "L": "7"} 

        for y, row in enumerate(self._grid):
            inside = False
            enter = ""
            for x, cell in enumerate(row):
                on_loop = (x, y) in loop_cells
                if on_loop:
                    if cell in topo_changing_pair:
                        enter = cell
                    elif cell == "|" or cell == topo_changing_pair.get(enter):
                        inside = not inside
                yield x, y, cell, "PATH" if on_loop else "IN" if inside else "OUT"

                if __debug__: print(pretty.get(cell, cell) if on_loop else "\033[1;96mI\033[0m" if inside else "\033[1;31mO\033[0m", end="")
            if __debug__: print()


def solve_1(data: str):
    grid = Grid(data)
    sx, sy = grid.find_start()
    size = sum(1 for _ in grid.walk_loop(sx, sy))
    return str(size // 2)


def solve_2(data: str):
    grid = Grid(data)
    total_inside = sum(1 for _, _, _, topo in grid.scan_topology() if topo == "IN")
    return str(total_inside)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
