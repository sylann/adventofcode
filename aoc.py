#!/usr/bin/env python3
import argparse
import stat
import subprocess
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

By default, scripts are run in optimized mode (no debug messages).
See --debug for more info.

ABOUT AUTHENTICATION

To download puzzles from the website, a cookie header is required.
This scripts expects to find the cookie string in `./.cookie`.

The file must be crated manually, and must contain a valid cookie. To get one,
authenticate on the website, then take the "Cookie" header from a request using
your browser debugger, and then copy & paste it in the .cookie file.
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
Use an example input file instead of the user specific input file.

The example file is created if missing but its content must be retrieved manually
from the website's puzzle description (it can't reliably be scrapped from the page).

EXAMPLES:
    aoc 2022 6 -e        ->  inputs/year_2022/day_06_example.txt
    aoc 2022 6 -e 1      ->  inputs/year_2022/day_06_example_1.txt
    aoc 2022 6 -e hello  ->  inputs/year_2022/day_06_example_hello.txt
"""

p.add_argument("-d", "--debug", action="store_true").help = """\
Enable debugging mode (disable optimization) and write debug messages to `debug.log`.
"""

p.add_argument("-l", "--lang", default="py", choices=directory_by_lang).help = """\
The file extension of the desired programming language.

Used to generate the correct solution file if it does not yet exist.
Controls what language is used to solve the puzzle.

Defaults to "py".
"""

p.add_argument("--timeout", type=int, default=5).help = """\
Interrupt execution if it takes more than the given time in seconds.

Defaults to 5 seconds.
"""



class Args(argparse.Namespace):
    year: int
    day: int
    lang: str
    example: bool | str
    debug: bool
    timeout: int


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


if not args.example and not input_file_user.exists():
    print(f"[INFO] Retrieving input from {aoc_url}")

    req = urllib.request.Request(aoc_url, method="GET")
    req.add_header("Cookie", aoc_cookie)

    with urllib.request.urlopen(req) as res:
        text = res.read().decode()

    print(f"[INFO] Writing input file")

    input_file_user.parent.mkdir(parents=True, exist_ok=True)
    input_file_user.write_text(text)


if not input_file_example.exists():
    print(f"[INFO] Writing example file (no content)")

    input_file_example.parent.mkdir(parents=True, exist_ok=True)
    input_file_example.touch()


if not code_file.exists():
    print(f"[INFO] Writing solution file")

    content = template_file.read_text() if template_file.exists() else ""

    code_file.parent.mkdir(parents=True, exist_ok=True)
    code_file.write_text(content)
    code_file.chmod(code_file.stat().st_mode | stat.S_IXUSR)  # chmod u+x


# TODO: handle more languages
if args.lang == "py":
    if args.debug:
        CMD = f"python {code_file} < {input_file} 2> debug.log"
    else:
        CMD = f"python -O {code_file} < {input_file}"

    print(CMD)
    subprocess.run(CMD, shell=True, timeout=args.timeout)
