from py.utils.debug import eprint


def iter_grids(data: str):
    grids = data.strip().split("\n\n")
    for grid in grids:
        grid = grid.split("\n")
        W = len(grid[0])
        H = len(grid)
        yield grid, W, H


def iter_symetric(mid: int, max1: int, max2):
    for delta in range(min(mid, max1 - mid)):
        before = mid - delta - 1
        after = mid + delta
        for i in range(max2):
            yield before, after, i


def summarize_notes(data: str, allowed_fixes: int) -> int:
    total = 0

    for grid, W, H in iter_grids(data):
        for m in range(1, W):
            smudges = sum(1 for L, R, y in iter_symetric(m, W, H) if grid[y][L] != grid[y][R])
            if smudges == allowed_fixes:
                total += m
        for m in range(1, H):
            smudges = sum(1 for U, D, x in iter_symetric(m, H, W) if grid[U][x] != grid[D][x])
            if smudges == allowed_fixes:
                total += m * 100
    return total


def solve_1(data: str):
    return str(summarize_notes(data, allowed_fixes=0))


def solve_2(data: str):
    return str(summarize_notes(data, allowed_fixes=1))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
