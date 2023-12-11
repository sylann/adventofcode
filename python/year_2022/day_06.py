#!/usr/bin/env python3
import collections
import sys

__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----


def find_marker(data: str, marker_size: int) -> int:
    assert len(data) >= marker_size, "puzzle doesn't mention missing characters"

    window = collections.deque(maxlen=marker_size)

    __(f"")
    __(f"   i window c (marker_size={marker_size})")
    for i, c in enumerate(data):
        __(f"{i:>4} {''.join(window)} {c}")
        if c in window:
            while c != window.popleft():
                pass

        window.append(c)
        if len(window) == marker_size:
            return i + 1

    assert False, "puzzle doesn't mention missing marker"


if __name__ == "__main__":
    data = sys.stdin.read()
    print("[PART 1]", find_marker(data, 4), sep="\n")
    print("[PART 2]", find_marker(data, 14), sep="\n")
