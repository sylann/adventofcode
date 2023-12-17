import sys
def eprint(*a, **kw): print(*a, **kw, file=sys.stderr)


def iter_cpu_cycles(program: str):
    reg_x = 1

    for line in program.strip("\n").split("\n"):
        match line.split():
            case ["addx", v]:
                yield reg_x
                yield reg_x
                reg_x += int(v)
            case ["noop"]:
                yield reg_x


def sum_signal_strengths(program: str) -> int:
    cycles_to_measure = iter((20, 60, 100, 140, 180, 220))
    to_measure = next(cycles_to_measure)
    strength = 0

    for cycle, reg_x in enumerate(iter_cpu_cycles(program), start=1):
        if cycle == to_measure:
            strength += cycle * reg_x
            if not (to_measure := next(cycles_to_measure, None)):
                break

    return strength


def print_crt(program: str) -> str:
    pixels = []
    for cycle, reg_x in enumerate(iter_cpu_cycles(program), start=0):
        reg_x_index = cycle % 40
        sprite_visible = reg_x - 1 <= reg_x_index <= reg_x + 1
        pixel = "#" if sprite_visible else "."
        pixels.append(pixel)

    line_width = 40
    return "\n".join(
        "".join(pixels[line_start: line_start + line_width])
        for line_start in range(0, len(pixels), line_width)
    )


if __name__ == "__main__":
    data = sys.stdin.read()
    print("[PART 1]", sum_signal_strengths(data), sep="\n")
    print("[PART 2]", print_crt(data), sep="\n")
