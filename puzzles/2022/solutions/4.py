#!/usr/bin/env python3
import sys
import typing as t

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----


class Range(t.NamedTuple):
    start: int
    end: int

    def contains(self, other: "Range") -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: "Range") -> bool:
        return not (self.start > other.end or other.start > self.end)


def count_needed_reviews(data: str, not_ok: t.Callable[[Range, Range], bool]):
    total = 0
    for line in data.strip().split("\n"):
        a1, a2 = line.split(",")
        r1 = Range(*map(int, a1.split("-")))
        r2 = Range(*map(int, a2.split("-")))
        if not_ok(r1, r2):
            total += 1
    return total


print("1:", count_needed_reviews(data, not_ok=lambda a, b: a.contains(b) or b.contains(a)))
print("2:", count_needed_reviews(data, not_ok=lambda a, b: a.overlaps(b)))
