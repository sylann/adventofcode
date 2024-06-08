turns = {"U": (0,-1), "D": (0,1), "L": (-1,0), "R": (1,0)}


def decode_line_1(line: str):
    d, l, _ = line.split()
    (dx, dy), l = turns[d], int(l)
    return dx, dy, l


def decode_line_2(line: str):
    l = int(line[-7:-2], 16)
    d = "RDLU"[int(line[-2])]
    dx, dy = turns[d]
    return dx, dy, l


def count_total_volume(data: str, decode_line) -> int:
    cx = cy = 0
    total = 0
    for line in data.strip().split("\n"):
        dx, dy, length = decode_line(line)
        nx = cx + dx * length
        ny = cy + dy * length
        total += cx * ny - cy * nx + length  # Gauss shoelace formula, + length for perimeter
        cx = nx
        cy = ny

    return total // 2 + 1 # round up


def solve_1(data: str):
    return count_total_volume(data, decode_line_1)


def solve_2(data: str):
    return count_total_volume(data, decode_line_2)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
