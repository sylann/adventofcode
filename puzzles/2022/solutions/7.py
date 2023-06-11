#!/usr/bin/env python3
import dataclasses
import sys
import typing as t

data = sys.stdin.read()
__ = lambda x: sys.stderr.write(f"[DEBUG] {x}\n")

# ----- START OF SOLUTION -----


@dataclasses.dataclass
class Node:
    name: str
    size: int = 0
    parent: t.Optional["NodeDir"] = None

    def __str__(self) -> str:
        raise NotImplementedError

    def walk(self, depth=0):
        raise NotImplementedError

    def notify_size_update(self, size_diff: int):
        if self.parent:
            self.parent.size += size_diff
            self.parent.notify_size_update(size_diff)


@dataclasses.dataclass
class NodeFile(Node):
    def __post_init__(self):
        self.notify_size_update(self.size)

    def __str__(self) -> str:
        return f"{self.name} (file, size={self.size})"

    def walk(self, depth=0):
        yield self, depth


@dataclasses.dataclass
class NodeDir(Node):
    children: list[Node] = dataclasses.field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name} (dir)"
    
    def walk(self, depth=0):
        yield self, depth
        for c in self.children:
            yield from c.walk(depth + 1)

    def get_child(self, name: str) -> Node | None:
        for c in self.children:
            if c.name == name:
                return c


def reconstruct_file_tree(terminal_output: str) -> NodeDir:
    root = NodeDir("/")

    cwd = root

    for line in terminal_output.split("\n"):
        match line.split():
            case ["$", "cd", "/"]:
                cwd = root
            case ["$", "cd", ".."]:
                cwd = cwd.parent or root
            case ["$", "cd", name]:
                child = cwd.get_child(name)
                if isinstance(child, NodeDir):
                    cwd = child
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                if not cwd.get_child(name):
                    cwd.children.append(NodeDir(name, parent=cwd))
            case [size, name]:
                if not cwd.get_child(name):
                    cwd.children.append(NodeFile(name, parent=cwd, size=int(size)))
            case x:
                __(f"Unhandled case: {x}")

    return root


def sum_size_of_smallest_dirs(tree: NodeDir, max_size: int) -> int:
    for node, depth in tree.walk():
        __("  " * depth + f"- {node}")

    return sum(n.size for n, _ in tree.walk() if isinstance(n, NodeDir) and n.size < max_size)


def find_dir_to_delete_for_update(tree: NodeDir, disk_size: int, update_size: int):
    free_space = disk_size - tree.size
    missing_space = max(0, update_size - free_space)

    assert missing_space > 0, "puzzle doesn't mention case with no missing space"

    # find the smallest dir that is bigger than missing_space
    return min(n.size for n, _ in tree.walk() if n.size > missing_space)


tree = reconstruct_file_tree(data)

print("1:", sum_size_of_smallest_dirs(tree, max_size=100000))
print("2:", find_dir_to_delete_for_update(tree, disk_size=70000000, update_size=30000000))
