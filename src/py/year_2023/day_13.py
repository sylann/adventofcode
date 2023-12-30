from py.utils.debug import eprint


def iter_grids(data: str):
    grids = data.strip().split("\n\n")
    for grid in grids:
        grid = grid.split("\n")
        W = len(grid[0])
        H = len(grid)
        yield grid, W, H


def is_symetric(lines: list[str], size: int, i_mirror: int, allowed_fixes: int):
    half_size = min(i_mirror, size-i_mirror) # min between left and right
    if __debug__: eprint(f"CHECK REFLEXION   {i_mirror-1:_>{half_size}}|{i_mirror:_<{half_size}} ({len(lines)} lines)")
    n_diffs = 0
    for j, line in enumerate(lines):
        left, right = line[i_mirror-half_size:i_mirror], line[i_mirror:i_mirror+half_size]
        if __debug__: eprint(f" {j:>2}  {line[:i_mirror]}|{line[i_mirror:]}   {left}|{right}")
        for i in range(half_size):
            i1 = i_mirror - i - 1
            i2 = i_mirror + i
            if line[i1] != line[i2]:
                if n_diffs == allowed_fixes:
                    return False
                n_diffs += 1
    if n_diffs:
        if __debug__: eprint(f"  DIFFS: {n_diffs}")
        if n_diffs == 1:
            return True
        return False

    return True


def find_symetry(lines: list[str], size: int, fix_allowed: bool) -> int | None:
    for i_mirror in range(1, size):
        if is_symetric(lines, size, i_mirror, fix_allowed):
            return i_mirror


def summarize_notes(data: str, allowed_fixes: int) -> int:
    total = 0

    for grid, W, H in iter_grids(data):
        if __debug__: eprint(f"{W}x{H}", *grid, sep="\n", end="\n\n")
        sym = find_symetry(grid, W, allowed_fixes)  # vertical reflexion
        if sym is not None:
            total += sym
            if __debug__: eprint(f"RESULT ┃ ", f"{sym-1:>2}|{sym:<2}")
            continue  # vertical reflexion takes priority (no double reflexion, yet)

        transposed = ["".join(col) for col in zip(*grid)]
        sym = find_symetry(transposed, H, allowed_fixes)  # horizontal reflexion
        if sym is not None:
            total += sym * 100
            if __debug__: eprint(f"RESULT ━ ", f"{sym-1:>2}|{sym:<2}")
        else:
            if __debug__: eprint(f"RESULT NO SYMETRY")

    return total


def solve_1(data: str):
    return str(summarize_notes(data, allowed_fixes=0))


def solve_2(data: str):
    return str(summarize_notes(data, allowed_fixes=1))


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
