import typing as t

from py.utils.debug import eprint


class MapRange(t.NamedTuple):
    dst: int
    src: int
    size: int


class Almanac:
    def __init__(self, data: str) -> None:
        """Parse seeds and maps from the given data"""
        seeds_line, _, *lines = data.strip().split("\n")
        self.seeds = [int(x) for x in seeds_line.removeprefix("seeds: ").split()]
        self.maps: dict[str, tuple[str, list[MapRange]]] = {}
        cur = None
        for line in lines:
            if cur is None:
                assert line.endswith(" map:")
                src, dst = line.removesuffix(" map:").split("-to-")  #soil-to-fertilizer map:
                cur = self.maps[src] = (dst, [])
            elif not line:
                cur = None
            else:
                cur[1].append(MapRange(*map(int, line.split())))

    def convert(self, cat: str, target: str, num: int, n_after=1) -> tuple[int, int]:
        """Convert a value "num" from category "cat" to category "target".

        n_after keeps track of the maximum amount of values that can be skipped.
        Values after "num" can be skipped because they will always be bigger.
        But map ranges are not "aligned". A value at the end of a category could
        lead to the start of another category.
        Reducing the number of values with each category is equivalent to finding
        a range that goes "straight" across all categories until target is reached.
        """
        if __debug__: eprint(num, end=" -> ")
        if cat == target:
            if __debug__: eprint(num, "skippable:", n_after)
            return num, n_after

        next_cat, ranges = self.maps[cat]
        for i_dst, i_src, size in ranges:
            if i_src <= num < i_src + size:
                n_before = num - i_src
                n_after = min(n_after, size - n_before)
                num = i_dst + n_before
                break

        return self.convert(next_cat, target, num, n_after)

    def __str__(self):
        return "".join(
            f"[Category Map: {src} -> {dst}]\n"
            + "".join(f"    {r}\n" for r in ranges)
            for src, (dst, ranges) in self.maps.items()    
        )


def solve_1(data: str):
    alma = Almanac(data)
    if __debug__: eprint(alma)

    minloc = 10**15  # Largely enough
    for seed in alma.seeds:
        loc, _ = alma.convert("seed", "location", seed)
        minloc = min(minloc, loc)
    return minloc


def solve_2(data: str):
    alma = Almanac(data)
    if __debug__: eprint(alma)

    minloc = 10**15  # Largely enough
    for i in range(0, len(alma.seeds), 2):
        seed, n_seeds = alma.seeds[i:i+2]
        while n_seeds > 0:
            loc, skip = alma.convert("seed", "location", seed, n_seeds)
            minloc = min(minloc, loc)
            seed += skip
            n_seeds -= skip
    return minloc


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
