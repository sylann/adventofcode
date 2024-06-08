from collections import namedtuple
import contextlib


def read_data(data: str):
    workflow, ratings = data.strip().split("\n\n")

    workflow_by_id = {}
    for line in workflow.split("\n"):
        name, content = line.removesuffix("}").split("{")
        rules = []
        for x in content.split(","):
            cond, _, result = x.rpartition(":")
            rules.append((cond, result))
        workflow_by_id[name] = rules

    return workflow_by_id, ratings


def solve_1(data: str):
    workflows, ratings = read_data(data)

    Part = namedtuple("Part", "x m a s")
    parts = [eval(f"Part({line[1:-1]})") for line in ratings.split("\n")]

    def eval_part(workflows, _part: Part):
        if __debug__: print(_part, end=": ")

        name = "in"
        while True:  # should be interrupted by a return
            if __debug__: print(name, end=" -> ")

            rules = workflows[name]  # should not fail
            for expr, result in rules:
                if not expr or eval(f"_part.{expr}"):
                    if result == "A":
                        if __debug__: print("A")
                        return True

                    elif result == "R":
                        if __debug__: print("R")
                        return False

                    name = result
                    break

    return sum(sum(p) for p in parts if eval_part(workflows, p)) 


class CombinationsCounter:
    def __init__(self, workflows) -> None:
        self.workflows = workflows
        for name in "xmas":
            setattr(self, f"{name}lo", 1)
            setattr(self, f"{name}hi", 4000)

        self.path = []
        self.all = (4000-1+1) ** 4
        self.accepted = 0
        self.rejected = 0
        self._walk_job("in")
        if __debug__: print("[Count Error]", self.rejected + self.accepted - self.all)

    def _walk_job(self, name):
        if name == "A":
            self.accepted += self._count_combinations()
        elif name == "R":
            self.rejected += self._count_combinations()
        else:
            rules = self.workflows[name]
            self._walk_rules(rules)

    def _count_combinations(self):
        out = 1
        for name in "xmas":
            lo = getattr(self, f"{name}lo")
            hi = getattr(self, f"{name}hi")
            out *= (hi-lo+1)

            if __debug__: print(f"{f'{name}={lo}:{hi}':<12}", end=" ")
            assert hi > lo
        if __debug__: print(", ".join(self.path), "     ",out)

        return out

    def _walk_rules(self, rules):
        if rules:
            cond, result = rules[0]
            if not cond:
                self._walk_job(result)
            else:
                with self._minmax_ctx(cond, reverse=False):
                    self._walk_job(result)
                with self._minmax_ctx(cond, reverse=True):
                    self._walk_rules(rules[1:])

    @contextlib.contextmanager
    def _minmax_ctx(self, cond: str, reverse: bool):
        def _ctx(key, min_or_max, bound):
            old_v = getattr(self, key)
            new_v = min_or_max(bound, old_v)
            setattr(self, key, new_v)
            yield
            setattr(self, key, old_v)

        name = cond[0]
        sign = cond[1]
        v = int(cond[2:])

        if __debug__: self.path.append(("!" if reverse else "") + cond)

        if reverse:
            if sign == "<": yield from _ctx(f"{name}lo", max, v)
            else:           yield from _ctx(f"{name}hi", min, v)
        else:
            if sign == "<": yield from _ctx(f"{name}hi", min, v-1)
            else:           yield from _ctx(f"{name}lo", max, v+1)

        if __debug__: self.path.pop()


def solve_2(data: str):
    workflows, _ = read_data(data)
    return CombinationsCounter(workflows).accepted


if __name__ == "__main__":
    import sys

    data = sys.stdin.read()
    print("\n[PART 1]", solve_1(data), sep="\n")
    print("\n[PART 2]", solve_2(data), sep="\n")
