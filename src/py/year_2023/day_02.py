rule = {"red": 12, "green": 13, "blue": 14}


def iter_game_info(data: str):
    for game_str in data.strip().split("\n"):
        id_, sets_str = game_str.removeprefix("Game ").split(": ")
        yield id_, list(iter_game_sets(sets_str))


def iter_game_sets(sets_str: str):
    game_sets = sets_str.split("; ")
    for game_set in game_sets:
        for x in game_set.split(", "):
            qty, color = x.split()
            yield int(qty), color


def game_is_valid(game_sets: list[tuple[int, str]]):
    for qty, color in game_sets:
        if qty > rule[color]:
            return False
    return True


def solve_1(data: str) -> int:
    total = 0
    for id_, game_sets in iter_game_info(data):
        if game_is_valid(game_sets):
            total += int(id_)
    return total


def compute_power(game_sets: list[tuple[int, str]]) -> int:
    maxes = {"red": 0, "green": 0, "blue": 0}
    for qty, color in game_sets:
        if qty > maxes[color]:
            maxes[color] = qty
    return maxes["red"] * maxes["green"] * maxes["blue"]


def solve_2(data: str) -> int:
    total = 0
    for id_, game_sets in iter_game_info(data):        
        total += compute_power(game_sets)
    return total


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
