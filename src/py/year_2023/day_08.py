from itertools import cycle
import typing as t

from py.utils.debug import eprint

class Branch(t.NamedTuple):
    L: str
    R: str

    def __getitem__(self, v: str) -> str:
        return getattr(self, v)


def solve_1(data: str):
    ins_str, _, *graph_str = data.strip().split("\n")

    graph: dict[str, Branch] = {}
    for line in graph_str:
        src, dsts = line.split(" = ")
        graph[src] = Branch(*dsts[1:-1].split(", "))

    cur, steps = "AAA", 1
    for dir in cycle(ins_str):
        dst = graph[cur][dir]
        if dst == "ZZZ":
            break
        cur = dst
        steps += 1

    return str(steps)

def solve_2(data: str):
    pass


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
