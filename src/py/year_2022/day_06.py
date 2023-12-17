import collections

from py.utils.debug import eprint


def find_marker(data: str, marker_size: int) -> int:
    assert len(data) >= marker_size, "puzzle doesn't mention missing characters"

    window = collections.deque(maxlen=marker_size)

    if __debug__: eprint(f"\n   i window c (marker_size={marker_size})")
    for i, c in enumerate(data):
        if __debug__: eprint(f"{i:>4} {''.join(window)} {c}")
        if c in window:
            while c != window.popleft():
                pass

        window.append(c)
        if len(window) == marker_size:
            return i + 1

    assert False, "puzzle doesn't mention missing marker"


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("[PART 1]", find_marker(data, 4), sep="\n")
    print("[PART 2]", find_marker(data, 14), sep="\n")
