import functools
from py.utils.debug import eprint


def iter_parts(data: str, unfold: int):
    for line in data.strip().split("\n"):
        parts, kd = line.split(" ")
        if unfold > 0:
            # unfold=5  ???.### 1,1,3  ->  ???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
            parts = "?".join([parts] * unfold)
            kd = ",".join([kd] * unfold)
        known_defect_sizes = [int(x) for x in kd.split(",")]
        yield parts, known_defect_sizes


def count_bad(parts: str, sizes: list[int]) -> int:
    n_parts = len(parts)
    total = 0

    def advance_good(prev: str, i: int, bad_chunks: list[int], bad_chunk: int) -> None:
        if prev == "#":
            dfs(".", i + 1, [*bad_chunks, bad_chunk], 0)
        else:
            dfs(".", i + 1, bad_chunks, 0)

    def advance_bad(i: int, bad_chunks: list[int], bad_chunk: int) -> None:
        dfs("#", i + 1, bad_chunks, bad_chunk + 1)

    def dfs(prev_part: str, i: int, bad_chunks: list[int], bad_chunk: int) -> None:
        if i == n_parts:
            if bad_chunk:
                bad_chunks = [*bad_chunks, bad_chunk]
            if bad_chunks == sizes:
                nonlocal total
                total += 1
            return
        
        part = parts[i]
        if part == "#":
            advance_bad(i, bad_chunks, bad_chunk)
        elif part == ".":
            advance_good(prev_part, i, bad_chunks, bad_chunk)
        else:
            assert part == "?"
            advance_bad(i, bad_chunks, bad_chunk)
            advance_good(prev_part, i, bad_chunks, bad_chunk)

    dfs("", 0, [], 0)
    return total


@functools.cache
def consume(parts: str, size: int):
    match = 0
    strict_start = -1
    end = len(parts) - 1
    for i, p in enumerate(parts):
        if p == ".":
            match = 0
            strict_start = -1
            continue

        if strict_start == -1 and p == "#":
            strict_start = i
            # print("STR [", parts, strict_start)

        match += 1
        if match >= size and (i == end or parts[i+1] != "#"):
            yield i+1

        if strict_start > -1 and i - strict_start == size:
            # print("    ]", parts, strict_start+size)
            break


def count(parts: str, sizes: list[int]) -> int:
    total = 0
    path = []

    def dfs(parts: str, i_size: int):
        if i_size == len(sizes):
            nonlocal total
            total += 1
            print(f"{total:>5}", ".".join(path))
            return
        size = sizes[i_size]
        if len(parts) < size:
            return

        for match_end in consume(parts, size):
            match_start = match_end-size
            path.append(parts[:match_start].replace("?", ".") + parts[match_start:match_end])
            remaining = parts[match_end+1:] # Skip 1 part, matches must be separated by a "."
            dfs(remaining, i_size + 1)
            path.pop()

    dfs(parts, 0)

    return total


def solve_1(data: str):
    total = 0
    for parts, defect_sizes in iter_parts(data, unfold=0):
        if __debug__: eprint("CASE:", parts, defect_sizes)
        total += count(parts, defect_sizes)
    return str(total)


def solve_2(data: str):
    total = 0
    for parts, defect_sizes in iter_parts(data, unfold=5):
        if __debug__: eprint("CASE:", parts, defect_sizes)
        total += count(parts, defect_sizes)
    return str(total)


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
