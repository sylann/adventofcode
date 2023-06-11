#!/usr/bin/env python3
import sys

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----

elfs = [sum(map(int, elf.split("\n"))) for elf in data.strip().split("\n\n")]
elfs.sort(reverse=True)

print("1:", elfs[0])
print("2:", sum(elfs[:3]))
