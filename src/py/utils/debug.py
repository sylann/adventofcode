import sys


def eprint(*args, **kwargs):
    """Print like the builtin print but write to stderr instead."""
    print(*args, **kwargs, file=sys.stderr)
