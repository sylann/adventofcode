from heapq import heappop, heappush


def cost_to_target(data: str, min_streak: int, max_streak: int):
    G = [[int(c) for c in line] for line in data.strip().split("\n")]
    W, H = len(G[0]), len(G)
    S = set()
    Q = [(0, 0, 0, 1, 0, 0)]

    while Q:
        loss, x, y, dx, dy, streak = heappop(Q)

        if streak >= min_streak and x == W-1 and y == H-1:
            return loss # found minimum possible heat loss

        if (x, y, dx, dy, streak) not in S:
            S.add((x, y, dx, dy, streak))

            if streak < max_streak: # explore straight ahead
                nx = x + dx
                ny = y + dy
                if 0 <= nx < W and 0 <= ny < H: # in bound only
                    heappush(Q, (loss + G[ny][nx], nx, ny, dx, dy, streak+1))

            if streak >= min_streak: # explore left and right
                for ndx, ndy in ((dy, dx), (-dy, -dx)):
                    nx = x + ndx
                    ny = y + ndy
                    if 0 <= nx < W and 0 <= ny < H: # in bound only
                        heappush(Q, (loss + G[ny][nx], nx, ny, ndx, ndy, 1))


def solve_1(data: str) -> str:
    return str(cost_to_target(data, min_streak=0, max_streak=3))


def solve_2(data: str) -> str:
    return str(cost_to_target(data, min_streak=4, max_streak=10))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
