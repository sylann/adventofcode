import enum
import typing as t
from py.utils.debug import eprint


class Shape(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(enum.IntEnum):
    Win = 6
    Draw = 3
    Lose = 0


shape_by_code         = {"A": Shape.Rock,   "B": Shape.Paper,  "C": Shape.Scissors}
shape_by_guessed_code = {"X": Shape.Rock,   "Y": Shape.Paper,  "Z": Shape.Scissors}
outcome_by_code       = {"X": Outcome.Lose, "Y": Outcome.Draw, "Z": Outcome.Win   }

winner_by_loser = {
    Shape.Rock: Shape.Paper,
    Shape.Paper: Shape.Scissors,
    Shape.Scissors: Shape.Rock,
}
loser_by_winner = {v: k for k, v in winner_by_loser.items()}

outcome_by_rshape_by_lshape = {
    s: {
        winner_by_loser[s]: Outcome.Win,
        s: Outcome.Draw,
        loser_by_winner[s]: Outcome.Lose,
    }
    for s in Shape
}

rshape_by_outcome_by_lshape = {
    l: {o: r for r, o in o_by_r.items()}
    for l, o_by_r in outcome_by_rshape_by_lshape.items()
}

DecodedLine = tuple[Shape, Shape, Outcome]
FInterpretLine = t.Callable[[str], DecodedLine]


def guess_meaning(line: str) -> DecodedLine:
    left = shape_by_code[line[0]]
    right = shape_by_guessed_code[line[2]]
    outcome = outcome_by_rshape_by_lshape[left][right]
    return left, right, outcome


def decode_meaning(line: str) -> DecodedLine:
    left = shape_by_code[line[0]]
    outcome = outcome_by_code[line[2]]
    right = rshape_by_outcome_by_lshape[left][outcome]
    return left, right, outcome


def get_final_score(data: str, interpret: FInterpretLine) -> int:
    total = 0

    for line in data.strip().split("\n"):
        # Example line: "A X"
        l, r, o = interpret(line)

        if __debug__: eprint(f"{r.name:<8} {l.name:<8}  {r} + {o} = {r + o}")

        total += r + o

    return total


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("[PART 1]", get_final_score(data, guess_meaning), sep="\n")
    print("[PART 2]", get_final_score(data, decode_meaning), sep="\n")
