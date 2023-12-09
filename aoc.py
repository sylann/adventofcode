#!/usr/bin/env python3
import argparse
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path


directory_by_lang = {
    "py": "python",
}

DESCRIPTION = """\
Shortcut script to prepare and run a solution to a puzzle of https://adventofcode.com.

By default, the script is executed with the input that is generated specifically
for the authenticated user. If missing, this input must be downloaded from the
website which requires being authenticated. See --example for more info.

By default, messages from stderr are not printed to the console.
See --debug for more info.

ABOUT AUTHENTICATION

Puzzle inputs are automatically downloaded from the website when needed and are
stored in a local folder for later reuse. But this requires authentication.
The website adventofcode.com manages authentication with a cookie header.
This scripts expects to find the cookie string in a local file (./.cookie by default).

To solve this problem once and for all, authenticate on the website,
retrieve the "Cookie" header from a request using your browser debugger and then
paste it in the .cookie file.
"""

p = argparse.ArgumentParser(
    description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

p.add_argument("year", type=int).help = """\
The year of the puzzle to execute. e.g. "2022", "2021"
"""

p.add_argument("day", type=int).help="""\
The day (or id) of the puzzle. e.g. "1", "2".
"""

p.add_argument("-e", "--example", nargs="?", default=False, const=True).help = """\
Execute the script with the example input from the website's puzzle description
instead of the one that is specific to the user.
The example file must have been created first. This is not done automatically.

Optionally give the suffix of an alternate example file to use instead of the
default one. Alternate example files must always have a path identical to the
default example with a suffix. e.g. `inputs/year_2022/day_06_example_<suffix>`.
This makes organisation consistent and cli use easy.
For example execute `./aoc.py 2022 6 -e hello` in your terminal to execute
`python/year_2022/day_06.py` with `inputs/year_2022/day_06_example_hello.txt`.
"""

p.add_argument("-d", "--debug", action="store_true").help = """\
Enable printing of stderr to the console, but limit the number of lines to an
arbitrary small number to prevent flooding.
"""

p.add_argument("--max-debug-lines", type=int, default=100).help = """\
Override the maximum number of stderr lines to print to the console.

For example, use a higher number to prevent truncating if necessary for debugging.
"""

p.add_argument("-l", "--lang", default="py", choices=directory_by_lang).help = """\
The extension of the file to generate. Default to "py".

Use this to choose a specific programming language to solve the puzzle.
This affects what file is executed.
If the file does not exist, a starting file is created at the appropriate path,
reusing the appropriate template if one is available.
"""


class Args(argparse.Namespace):
    year: int
    day: int
    lang: str
    example: bool | str
    debug: bool
    max_debug_lines: int


args = p.parse_args(namespace=Args())


directory = directory_by_lang[args.lang]
ex_id = "_example" + (f"_{args.example}" if isinstance(args.example, str) else "")

input_file_example = Path("inputs") / f"year_{args.year}" / f"day_{args.day:0>2}{ex_id}.txt"
input_file_user    = Path("inputs") / f"year_{args.year}" / f"day_{args.day:0>2}.txt"
code_file          = Path(directory) / f"year_{args.year}" / f"day_{args.day:0>2}.{args.lang}"
template_file      = Path(directory) / f"template.{args.lang}"

aoc_url = f"https://adventofcode.com/{args.year}/day/{args.day}/input"
aoc_cookie = Path(".cookie").read_text().strip()

input_file = input_file_example if args.example else input_file_user

print(f"[INFO] input_file: {input_file}")
print(f"[INFO] code_file: {code_file}")


if not args.example and not input_file_user.exists():
    print(f"[INFO] Retrieving input from {aoc_url}")

    req = urllib.request.Request(aoc_url, method="GET")
    req.add_header("Cookie", aoc_cookie)

    with urllib.request.urlopen(req) as res:
        text = res.read().decode()

    print(f"[INFO] Writing input file")

    input_file_user.parent.mkdir(parents=True, exist_ok=True)
    input_file_user.write_text(text)


if not code_file.exists():
    print(f"[INFO] Writing solution file")

    content = template_file.read_text() if template_file.exists() else ""

    code_file.parent.mkdir(parents=True, exist_ok=True)
    code_file.write_text(content)
    code_file.chmod(code_file.stat().st_mode | stat.S_IXUSR)  # chmod u+x


# TODO: handle compilation for rust files
executable = code_file


with open(input_file, mode="rt") as stdin:
    stdout=subprocess.PIPE
    stderr=subprocess.PIPE if args.debug else subprocess.DEVNULL

    p = subprocess.run([executable], stdin=stdin, stdout=stdout, stderr=stderr, text=True)

    if args.debug:
        sys.stderr.write("\n")
        sys.stderr.write("----- Program's stderr -----\n")

        excess_lines = p.stderr.count("\n") - args.max_debug_lines
        if excess_lines > 0:
            truncate_msg = [
                "-----",
                f"Content was too long, {excess_lines} lines were truncated.",
                "Use --max-debug-lines to control how many lines can be displayed.",
                "-----",
            ]
            lines = p.stderr.split("\n")
            n = args.max_debug_lines // 2
            sys.stderr.write("\n".join(lines[:n] + truncate_msg + lines[-n:]))
        else:
            sys.stderr.write(p.stderr)

    sys.stdout.write("\n")
    sys.stdout.write("----- Program's stdout -----\n")
    sys.stdout.write(p.stdout)

    exit(p.returncode)
