#!/usr/bin/env python3
import sys

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----


def sum_signal_strengths(program: str) -> int:
    cycles = [0]  # add 0 to simulate 1-based index
    reg_x = 1

    for line in program.strip("\n").split("\n"):
        match line.split():
            case ["addx", v]:
                cycles.append(reg_x)
                cycles.append(reg_x)
                reg_x += int(v)
            case ["noop"]:
                cycles.append(reg_x)

    cycles_to_measure = (20, 60, 100, 140, 180, 220)
    return sum(cycles[i] * i for i in cycles_to_measure)


print("1:", sum_signal_strengths(data))
print("2:", ...)
