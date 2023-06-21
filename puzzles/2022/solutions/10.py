#!/usr/bin/env python3
import sys

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----


def iter_cpu_cycles(program: str):
    reg_x = 1

    for line in program.strip("\n").split("\n"):
        match line.split():
            case ["addx", v]:
                yield reg_x
                yield reg_x
                reg_x += int(v)
            case ["noop"]:
                yield reg_x


def sum_signal_strengths(program: str) -> int:
    cycles_to_measure = iter((20, 60, 100, 140, 180, 220))
    to_measure = next(cycles_to_measure)
    strength = 0

    for cycle, reg_x in enumerate(iter_cpu_cycles(program), start=1):
        if cycle == to_measure:
            strength += cycle * reg_x
            if not (to_measure := next(cycles_to_measure, None)):
                break

    return strength

print("1:", sum_signal_strengths(data))
print("2:", ...)
