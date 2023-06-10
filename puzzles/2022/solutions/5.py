#!/usr/bin/env python3
import sys
import typing as t

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ---- START OF SOLUTION -----


class Procedure(t.NamedTuple):
    src: str
    dst: str
    repeat: int

    @classmethod
    def from_str(cls, proc: str):
        """Parses a string in the form "move %(repeat)d from %(src)s to %(dst)s"""
        _, n, _, src, _, dst = proc.split(" ")
        return Procedure(src=src, dst=dst, repeat=int(n))


class Cargo:
    def __init__(self, scheme: str):
        grid = scheme.split("\n")
        stack_ids = grid.pop().split()

        # Store stacks by str id to avoid unnecessary number parsing
        # and facilitate access when reading procedures.
        self.stacks: dict[str, list[str]] = {id: [] for id in stack_ids}

        for y in range(len(grid) - 1, -1, -1):
            for i, sid in enumerate(stack_ids):
                crate = grid[y][i * 4 + 1]
                if crate != " ":
                    self.stacks[sid].append(crate)

        __(f"stacks = {self.stacks}")

    def read_top_crates_ids(self) -> str:
        return "".join(stack[-1] for stack in self.stacks.values())


class Crane9000:
    def move_crates(self, cargo: Cargo, proc: Procedure) -> None:
        stacks, (s, d, n) = cargo.stacks, proc
        for _ in range(n):
            stacks[d].append(stacks[s].pop())


class Crane9001(Crane9000):
    def move_crates(self, cargo: Cargo, proc: Procedure) -> None:
        stacks, (s, d, n) = cargo.stacks, proc
        stacks[s], moved = stacks[s][:-n], stacks[s][-n:]
        stacks[d] += moved


def operate(data: str, Crane: type[Crane9000]):
    stacks_str, procs_str = data.rstrip("\n").split("\n\n")

    cargo = Cargo(stacks_str)
    crane = Crane()

    for x in procs_str.split("\n"):
        proc = Procedure.from_str(x) 
        __(proc)
        crane.move_crates(cargo, proc)

    return cargo.read_top_crates_ids()


print("1:", operate(data, Crane9000))
print("2:", operate(data, Crane9001))
