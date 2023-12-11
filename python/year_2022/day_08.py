#!/usr/bin/env python3
import sys
def eprint(*a, **kw): print(*a, **kw, file=sys.stderr)


TForest = tuple[list[list[int]], int, int]


def inspect_forest(forest_scheme: str) -> TForest:
    forest = [[int(c) for c in f] for f in forest_scheme.strip("\n").split("\n")]

    w, h = len(forest[0]), len(forest)

    if __debug__: eprint(f"forest = {forest}")
    if __debug__: eprint(f"w, h = {w}, {h}")

    return forest, w, h


def count_visible_trees(forest_scheme: str) -> int:
    forest, w, h = inspect_forest(forest_scheme)

    n_visible = (w + h - 2) * 2  # Outer trees are always visible
    if __debug__: eprint(f"n_visible = {n_visible}")

    for x in range(1, w-1):
        for y in range(1, h-1):
            tree = forest[y][x]
            if __debug__: eprint(f"x, y = {x}, {y}")

            n_visible += (
                   tree > max(forest[y][cx] for cx in range(x))       # left
                or tree > max(forest[y][cx] for cx in range(x+1, w))  # right
                or tree > max(forest[cy][x] for cy in range(y))       # up
                or tree > max(forest[cy][x] for cy in range(y+1, h))  # down
            )

    return n_visible


def get_max_scenic_score(forest_scheme: str) -> int:
    forest, w, h = inspect_forest(forest_scheme)

    max_score = 0

    for x in range(1, w-1):
        for y in range(1, h-1):
            tree = forest[y][x]

            vdl = vdr = vdu = vdd = 0
        
            for vdl, cx in enumerate(range(x-1,-1,-1), start=1):  # left
                if forest[y][cx] >= tree: break
            for vdr, cx in enumerate(range(x+1, w),    start=1):  # right
                if forest[y][cx] >= tree: break
            for vdu, cy in enumerate(range(y-1,-1,-1), start=1):  # up
                if forest[cy][x] >= tree: break
            for vdd, cy in enumerate(range(y+1, h),    start=1):  # down
                if forest[cy][x] >= tree: break

            if __debug__: eprint(f"x, y = {x}, {y}  score = {vdl} * {vdr} * {vdu} * {vdd}")
            max_score = max(max_score, vdl * vdr * vdu * vdd)

    return max_score


if __name__ == "__main__":
    data = sys.stdin.read()
    print("[PART 1]", count_visible_trees(data), sep="\n")
    print("[PART 2]", get_max_scenic_score(data), sep="\n")
