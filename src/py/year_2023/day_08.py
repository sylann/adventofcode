import math
import typing as t
from itertools import cycle

from py.utils.debug import eprint


class Branch(t.NamedTuple):
    L: str
    R: str

    def __getitem__(self, v: str) -> str:
        return getattr(self, v)


def build_graph(data: str):
    ins_str, _, *graph_str = data.strip().split("\n")
    graph: dict[str, Branch] = {}
    for line in graph_str:
        src, dsts = line.split(" = ")
        graph[src] = Branch(*dsts[1:-1].split(", "))
    return ins_str, graph


def solve_1(data: str):
    instructions, graph = build_graph(data)

    if "AAA" not in graph or "ZZZ" not in graph:
        return "BAD DATA: solve_1 is not compatible"

    cur, steps = "AAA", 1
    for dir in cycle(instructions):
        dst = graph[cur][dir]

        if dst == "ZZZ":
            break

        cur = dst
        steps += 1

    return str(steps)


def solve_2(data: str):
    instructions, graph = build_graph(data)

    paths = tuple(p for p in graph if p[2] == "A")

    steps = 1
    for src in paths:
        path_cycle = [src]
        seen: set[str] = set()

        for dir in cycle(instructions):
            dst = graph[src][dir]
            key = f"{dst} {dir}"
            path_cycle.append(key)

            if dst[2] == "Z" and key in seen:
                break

            src = dst
            seen.add(key)

        start = path_cycle.index(path_cycle[-1])
        size = len(path_cycle) - 1 - start
        steps = math.lcm(steps, size)  # immediate update, ok because LCMs are associative
        if __debug__: eprint(f"start={start} size={size} {', '.join(path_cycle)}")

    return str(steps)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
